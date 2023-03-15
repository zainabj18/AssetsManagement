from app.core.utils import protected,run_query,model_creator,QueryResult
from app.db import DataAccess, UserRole, get_db,Actions,Models
from app.schemas import Asset, AssetBaseInDB, AssetOut, AttributeInDB,FilterSearch,QueryOperation,Attribute_Model,Project,Comment,CommentOut
from flask import Blueprint, jsonify, request
from psycopg.rows import class_row, dict_row
from pydantic import ValidationError
from psycopg import Error
from app.auth.routes import get_user_by_id
from itertools import chain
from flask import abort
bp = Blueprint("asset", __name__, url_prefix="/asset")
import json
def asset_differ(orginal,new):
    removed=list(set(orginal.keys())-set(new.keys()))
    changed=[]
    added=list(set(new.keys())-set(orginal.keys()))
    for key in orginal:
        if key in new:
            if key=="metadata":
                old_values_dict={}
                new_values_dict={}
                for at in orginal["metadata"]:
                    print(at)
                    old_values_dict[at["attributeID"]]=at
                for at in new["metadata"]:
                    new_values_dict[at["attributeID"]]=at
                metadata_removed=list(set(old_values_dict.keys())-set(new_values_dict.keys()))
                metadata_added=list(set(new_values_dict.keys())-set(old_values_dict.keys()))
                for attribute in metadata_removed:
                    name=old_values_dict[attribute]["attributeName"]
                    removed.append(f"metadata-{attribute}-{name}")
                for attribute in metadata_added:
                    name=new_values_dict[attribute]["attributeName"]
                    added.append(f"metadata-{attribute}-{name}")
                print(old_values_dict)
                print(new_values_dict)
                for key in old_values_dict:
                    if key in new_values_dict:
                        if old_values_dict[key]["attributeValue"]!=new_values_dict[key]["attributeValue"]:
                            name=old_values_dict[key]["attributeName"]
                            changed.append((f"metadata-{key}-{name}",old_values_dict[key]["attributeValue"],new_values_dict[key]["attributeValue"]))    
            elif orginal[key]!=new[key]:
                if isinstance(orginal[key],list) and isinstance(new[key],list):
                    list_removed=list(set(orginal[key])-set(new[key]))
                    list_added=list(set(new[key])-set(orginal[key]))
                    changed.append((key,tuple(list_removed),tuple(list_added)))   
                else:
                    changed.append((key,orginal[key],new[key]))    

    return {"added":added,"removed":removed,"changed":changed}
def fetch_asset(db,id,classification):
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            # gets asset
            cur.execute(
                """SELECT * FROM assets WHERE asset_id=%(id)s AND soft_delete=0;""",
                {"id": id},
            )
            asset = cur.fetchone()
            # check user can view assset
            if asset.classification > classification:
                return {"data": []}, 401
        # get related info for asset
        with db_conn.cursor(row_factory=class_row(AttributeInDB)) as cur:
            cur.execute(
                """SELECT attributes.attribute_id,attribute_name, attribute_data_type as attribute_data_type, validation_data,value as attribute_value FROM attributes_values 
INNER JOIN attributes on attributes.attribute_id=attributes_values.attribute_id WHERE asset_id=%(id)s;""",
                {"id": id},
            )
            metadata = cur.fetchall()
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT projects.* FROM assets_in_projects
INNER JOIN projects on projects.id=assets_in_projects.project_id WHERE asset_id=%(id)s;""",
                {"id": id},
            )
            projects = [Project(**row).dict(by_alias=True) for row in cur.fetchall()]
            print(projects)
            cur.execute(
                """SELECT tags.id,name FROM assets_in_tags 
INNER JOIN tags on tags.id=assets_in_tags.tag_id WHERE asset_id=%(id)s;""",
                {"id": id},
            )
            tags = list(cur.fetchall())
            cur.execute(
                """SELECT assets.* FROM assets_in_assets
    INNER JOIN assets on assets.asset_id=assets_in_assets.to_asset_id WHERE from_asset_id=%(id)s;""",
                {"id": id},
            )
            assets = list(cur.fetchall())
            cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                {"version_id": asset.version_id},
            )
            type = cur.fetchone()["type_name"]

        asset = AssetOut(
            **asset.dict(), metadata=metadata, projects=projects, tags=tags,assets=assets,type=type
        )
    return asset

@bp.route("/", methods=["POST"])
@protected(role=UserRole.USER)
def create(user_id, access_level):
    # validate json
    try:
        try:
            asset = Asset(**request.json)
        except ValidationError as e:
            return (
                jsonify(
                    {
                        "msg": "Data provided is invalid",
                        "data": e.errors(),
                        "error": "Failed to create asset from the data provided",
                    }
                ),
                400,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": None,
                    "error": "Failed to create asset from the data provided",
                }
            ),
            400,
        )
    db = get_db()
    db_asset = asset.dict(exclude={"metadata"})
   

    print(db_asset)
    # add asset to db
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT version_id FROM assets WHERE asset_id=ANY(%(asset_ids)s);""",
                {"asset_ids":asset.assets})
            asset_types=set([x[0] for x in cur.fetchall()])
            cur.execute("""SELECT type_id_to FROM type_link WHERE type_id_from=%(type_id)s;""",{"type_id": asset.version_id})
            dependents= set([x[0] for x in cur.fetchall()])
            if not asset_types.issuperset(dependents):
                return (
                    jsonify(
                        {
                            "msg": "Missing dependencies",
                            "data": f"Must inlcude assets with type {dependents}",
                            "error": "Failed to create asset from the data provided",
                        }
                    ),
                    400,
                )
            cur.execute("""SELECT attributes_in_types.attribute_id FROM attributes_in_types
INNER JOIN attributes on attributes_in_types.attribute_id=attributes.attribute_id
WHERE (attributes.validation_data->>'isOptional')::boolean is false AND attributes_in_types.type_version=%(type_id)s;""",{"type_id": asset.version_id})
            required_attributes=set([x[0] for x in cur.fetchall()])
            attribute_ids=set([attribute.attribute_id for attribute in asset.metadata])
            cur.execute("""SELECT attributes_in_types.attribute_id FROM attributes_in_types
INNER JOIN attributes on attributes_in_types.attribute_id=attributes.attribute_id
WHERE attributes_in_types.type_version=%(type_id)s;""",{"type_id": asset.version_id})
            all_type_attributes=set([x[0] for x in cur.fetchall()])
            
            if not required_attributes.issubset(attribute_ids):
                 return (
                    jsonify(
                        {
                            "msg": "Missing required attributes",
                            "data": f"Must inlcude the following attrubutes with ids {list(required_attributes)}",
                            "error": "Failed to create asset from the data provided",
                        }
                    ),
                    400,
                )
            if not (attribute_ids.issubset(all_type_attributes)):
                return (
                    jsonify(
                        {
                            "msg": "Addtional attributes",
                            "data": f"Must only inlcude the following attrubutes with ids {list(all_type_attributes)}",
                            "error": "Failed to create asset from the data provided",
                        }
                    ),
                    400,
                )

            cur.execute(
                """
            INSERT INTO assets (name,link,version_id,description, classification)
    VALUES (%(name)s,%(link)s,%(version_id)s,%(description)s,%(classification)s)  RETURNING asset_id;""",
                db_asset,
            )
            asset_id = cur.fetchone()[0]
            # add asset to tags to db
            for tag in asset.tags:
                cur.execute(
                    """
                INSERT INTO assets_in_tags (asset_id,tag_id)
        VALUES (%(asset_id)s,%(tag_id)s);""",
                    {"asset_id": asset_id, "tag_id": tag},
                )
            for a in asset.assets:
                cur.execute(
                    """
                INSERT INTO assets_in_assets (from_asset_id,to_asset_id)
        VALUES (%(from_asset_id)s,%(to_asset_id)s);""",
                    {"from_asset_id": asset_id, "to_asset_id": a},
                )
            # add asset to projects to db
            for project in asset.projects:
                cur.execute(
                    """
                INSERT INTO assets_in_projects (asset_id,project_id)
        VALUES (%(asset_id)s,%(project_id)s);""",
                    {"asset_id": asset_id, "project_id": project},
                )
            # add attribute values to db
            for attribute in asset.metadata:
                cur.execute(
                    """
                INSERT INTO attributes_values (asset_id,attribute_id,value)
        VALUES (%(asset_id)s,%(attribute_id)s,%(value)s);""",
                    {
                        "asset_id": asset_id,
                        "attribute_id": attribute.attribute_id,
                        "value": attribute.attribute_value,
                    },
                )
            cur.execute(
                    """
                INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
        VALUES (1,%(account_id)s,%(asset_id)s,%(diff)s,%(action)s);""",
                    {"account_id":user_id,"asset_id":asset_id,"diff":json.dumps({}),"action":Actions.ADD},
                )
    return {"msg": "Added asset", "data": asset_id}, 200


@bp.route("/classifications", methods=["GET"])
@protected(role=UserRole.USER)
def get_classifications(user_id, access_level):
    viwable_classifications = []
    for c in DataAccess:
        if c <= access_level:
            viwable_classifications.append(c.value)

    return {"data": viwable_classifications}


@bp.route("projects/<id>", methods=["GET"])
def list_asset_project(id):
    db = get_db()
    # get related projects for asset and set them to be selected for easy rendering on UI
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT projects.* FROM assets_in_projects
    INNER JOIN projects on projects.id=assets_in_projects.project_id WHERE asset_id=%(id)s;""",
                {"id": id},
            )
            selected_projects = [Project(**row).dict(by_alias=True) for row in cur.fetchall()]
            
            for x in selected_projects:
                x["isSelected"] = True
            cur.execute(
                """SELECT * FROM projects WHERE id not in (SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s);""",
                {"id": id},
            )
            projects = [Project(**row).dict(by_alias=True) for row in cur.fetchall()]
            selected_projects.extend(projects)
    return {"data": selected_projects}, 200

@bp.route("links/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def list_asset_in_assets(id,user_id, access_level):
    db = get_db()
    # get related assets for  an asset and set them to be selected for easy rendering on UI
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
                """SELECT assets.* FROM assets_in_assets
    INNER JOIN assets on assets.asset_id=assets_in_assets.to_asset_id WHERE from_asset_id=%(id)s ORDER BY assets_in_assets.to_asset_id;""",
                {"id": id},
            )
            selected_assets = list(cur.fetchall())
            for x in selected_assets:
                x.isSelected = True
            cur.execute(
                """SELECT * FROM assets WHERE asset_id not in (SELECT to_asset_id FROM assets_in_assets WHERE from_asset_id=%(id)s) AND asset_id!=%(id)s ORDER BY asset_id;""",
                {"id": id},
            )
            assets = list(cur.fetchall())
            selected_assets.extend(assets)
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in selected_assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res




@bp.route("/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def view(id, user_id, access_level):
    #TODO view if none
    db = get_db()
    asset=fetch_asset(db,id,access_level)
    
    return {"data": json.loads(asset.json(by_alias=True))}, 200


@bp.route("/<id>", methods=["DELETE"])
def delete(id):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor() as cur:
            cur.execute(
                """UPDATE assets SET soft_delete = %(del)s WHERE asset_id=%(id)s;""",
                {"id": id, "del": 1},
            )

    return {}, 200




@bp.route("/summary", methods=["GET"])
@protected(role=UserRole.VIEWER)
def summary(user_id, access_level):
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute("""SELECT * FROM assets WHERE soft_delete=0 ORDER BY asset_id;""")
            assets = cur.fetchall()
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res


@bp.route("/<id>", methods=["PATCH"])
@protected(role=UserRole.VIEWER)
def update(id, user_id, access_level):
    db = get_db()
    asset = dict(**request.json)
    del asset['created_at']
    del asset['last_modified_at']
    orgignal_asset=fetch_asset(db,id,access_level)
    orgignal_asset=json.loads(orgignal_asset.json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    orgignal_asset["tags"]=[tag["id"]for tag in orgignal_asset["tags"]]
    orgignal_asset["projects"]=[project["projectID"]for project in orgignal_asset["projects"]]
    orgignal_asset["assets"]=[a["asset_id"]for a in orgignal_asset["assets"]]
    projects_removed=list(set(orgignal_asset["projects"])-set(asset["projects"]))
    projects_added=list(set(asset["projects"])-set(orgignal_asset["projects"]))
    assets_removed=list(set(orgignal_asset["assets"])-set(asset["assets"]))
    assets_added=list(set(asset["assets"])-set(orgignal_asset["assets"]))
    tags_removed=list(set(orgignal_asset["tags"])-set(asset["tags"]))
    tags_added=list(set(asset["tags"])-set(orgignal_asset["tags"]))
    diff_dict=asset_differ(orgignal_asset,asset)
    with db.connection() as conn:
        with conn.cursor() as cur:
            
            cur.execute(
                """SELECT version_id FROM assets WHERE asset_id=ANY(%(asset_ids)s);""",
                {"asset_ids":asset["assets"]})
            asset_types=set([x[0] for x in cur.fetchall()])
            cur.execute("""SELECT type_id_to FROM type_link WHERE type_id_from=%(type_id)s;""",{"type_id": asset["version_id"]})
            dependents= set([x[0] for x in cur.fetchall()])
            if not asset_types.issuperset(dependents):
                return (
                    jsonify(
                        {
                            "msg": "Missing dependencies",
                            "data": f"Must inlcude assets with type {dependents}",
                            "error": "Failed to create asset from the data provided",
                        }
                    ),
                    400,
                )
            cur.execute(
                    """
                INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
        VALUES (1,%(account_id)s,%(asset_id)s,%(diff)s,%(action)s);""",
                    {"account_id":user_id,"asset_id":asset["asset_id"],"diff":json.dumps(diff_dict),"action":Actions.CHANGE},
                )
            print(asset)
            cur.execute(
                """
            UPDATE assets 
            SET name=%(name)s,link=%(link)s,description=%(description)s,version_id=%(version_id)s,classification=%(classification)s,last_modified_at=now() WHERE asset_id=%(asset_id)s ;""",
                asset,
            )
            cur.execute("""
            DELETE FROM assets_in_tags WHERE tag_id = ANY(%(tag_ids)s) AND asset_id=%(asset_id)s;
            """,{"tag_ids":tags_removed,"asset_id":asset["asset_id"]})
            cur.execute("""
            DELETE FROM assets_in_projects WHERE project_id = ANY(%(project_ids)s) AND asset_id=%(asset_id)s;
            """,{"project_ids":projects_removed,"asset_id":asset["asset_id"]})
            cur.execute("""
            DELETE FROM assets_in_assets WHERE to_asset_id = ANY(%(asset_ids)s) AND from_asset_id=%(asset_id)s;
            """,{"asset_ids":assets_removed,"asset_id":asset["asset_id"]})
            for a in assets_added:
                cur.execute(
                    """
                INSERT INTO assets_in_assets (from_asset_id,to_asset_id)
        VALUES (%(from_asset_id)s,%(to_asset_id)s);""",
                    {"from_asset_id": asset["asset_id"], "to_asset_id": a},
                )
            for tag in tags_added:
                cur.execute(
                    """
                INSERT INTO assets_in_tags (asset_id,tag_id)
        VALUES (%(asset_id)s,%(tag_id)s);""",
                    {"asset_id": asset["asset_id"], "tag_id": tag},
                )
            # add asset to projects to db
            for project in projects_added:
                cur.execute(
                    """
                INSERT INTO assets_in_projects (asset_id,project_id)
        VALUES (%(asset_id)s,%(project_id)s);""",
                    {"asset_id": asset["asset_id"], "project_id": project},
                )
            # updates metadatat values
            print(asset["metadata"],"hello")
            for attribute in asset["metadata"]:
                # cur.execute(
                #     """
                # UPDATE attributes_values 
                # SET value=%(attributeValue)s WHERE asset_id=%(asset_id)s AND attribute_id=%(attributeID)s;""",
                #     {"asset_id": id, **attribute},
                # )
                cur.execute(
                    """
                INSERT INTO attributes_values (asset_id,attribute_id,value)
        VALUES (%(asset_id)s,%(attributeID)s,%(attributeValue)s) ON CONFLICT (asset_id,attribute_id) DO UPDATE
SET value = EXCLUDED.value""",
                    {
                        "asset_id": id,
                        **attribute
                    },
                )
            
    return {}, 200

@bp.route("/logs/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def logs(id, user_id, access_level):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT * FROM audit_logs
WHERE object_id=%(asset_id)s AND model_id=1
ORDER BY date ASC;""",
                {"asset_id": id},
            )
            logs = cur.fetchall()
            print(logs)
            for log in logs:
                if username := get_user_by_id(db,log["account_id"]):
                    username = username[0]
                log["username"]=username
    return {"data":logs}

@bp.route("/tags/summary/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def tags_summary(id, user_id, access_level):
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
                """SELECT assets.* FROM assets
INNER JOIN assets_in_tags ON assets.asset_id=assets_in_tags.asset_id WHERE soft_delete=0 AND tag_id=%(tag_id)s ORDER BY assets.asset_id;""",
                {"tag_id": id},
            )
            assets = cur.fetchall()
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT name FROM tags WHERE id=%(id)s;""",
                {"id": id},
            )
            tag = cur.fetchone()
            if tag:
                tag=tag["name"]
            else:
                return {"msg":"No tag id found"},400
            for a in assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": {"tag": tag, "assets": assets_json}})
    return res


@bp.route("/related/tags/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def related_tags(id,user_id, access_level):
    db = get_db()
    # get related assets for  an asset and set them to be selected for easy rendering on UI
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
                """
                WITH related_asset_tags as (SELECT COUNT(asset_id),asset_id FROM assets_in_tags WHERE tag_id in (SELECT tag_id FROM assets_in_tags WHERE asset_id=%(id)s) and asset_id !=%(id)s
GROUP BY asset_id
HAVING COUNT(asset_id)>0)
SELECT assets.*,related_asset_tags.count FROM assets
INNER JOIN related_asset_tags on assets.asset_id=related_asset_tags.asset_id
ORDER BY count DESC;""",
                {"id": id},
            )
            selected_assets = list(cur.fetchall())
 
            assets = list(cur.fetchall())
            selected_assets.extend(assets)
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in selected_assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res



@bp.route("/related/projects/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def related_projects(id,user_id, access_level):
    #get all the assets that belong to the same project as an asset
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
                """
                WITH related_asset_projects as (SELECT COUNT(asset_id),asset_id FROM assets_in_projects WHERE project_id in (SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s) and asset_id !=%(id)s
GROUP BY asset_id
HAVING COUNT(asset_id)>0)
SELECT assets.*,related_asset_projects.count FROM assets
INNER JOIN related_asset_projects on assets.asset_id=related_asset_projects.asset_id
ORDER BY count DESC;""",
                {"id": id},
            )
            selected_assets = list(cur.fetchall())
 
            assets = list(cur.fetchall())
            selected_assets.extend(assets)
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in selected_assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res

@bp.route("/related/classification/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def related_classification(id,user_id, access_level):
    #get all the assets that belong to the same project as an asset
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
                """
                SELECT * FROM assets WHERE classification=(SELECT classification FROM assets WHERE asset_id=%(id)s) AND asset_id!=%(id)s ORDER BY asset_id;""",
                {"id": id},
            )
            selected_assets = list(cur.fetchall())
 
            assets = list(cur.fetchall())
            selected_assets.extend(assets)
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in selected_assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res


@bp.route("/related/type/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def related_type(id,user_id, access_level):
    #get all the assets that belong to the same project as an asset
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
                """
                SELECT * FROM assets WHERE type=(SELECT type FROM assets WHERE asset_id=%(id)s) AND asset_id!=%(id)s ORDER BY asset_id;""",
                {"id": id},
            )
            selected_assets = list(cur.fetchall())
 
            assets = list(cur.fetchall())
            selected_assets.extend(assets)
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in selected_assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res


@bp.route("/related/from/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def related_from(id,user_id, access_level):
    #get all the assets that belong to the same project as an asset
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
"""SELECT assets.* FROM assets_in_assets
    INNER JOIN assets on assets.asset_id=assets_in_assets.to_asset_id WHERE from_asset_id=%(id)s ORDER BY assets_in_assets.to_asset_id;""",
                {"id": id},
            )
            selected_assets = list(cur.fetchall())
 
            assets = list(cur.fetchall())
            selected_assets.extend(assets)
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in selected_assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res


@bp.route("/related/to/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def related_to(id,user_id, access_level):
    #get all the assets that belong to the same project as an asset
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
"""SELECT assets.* FROM assets_in_assets
INNER JOIN assets on assets.asset_id=assets_in_assets.from_asset_id WHERE to_asset_id=%(id)s ORDER BY assets_in_assets.to_asset_id;""",
                {"id": id},
            )
            selected_assets = list(cur.fetchall())
 
            assets = list(cur.fetchall())
            selected_assets.extend(assets)
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in selected_assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
                        {"version_id": a.version_id},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": assets_json})
    return res


def make_query(searcher):
    match searcher.operation:
        case QueryOperation.EQUALS:
            query="SELECT asset_id FROM all_atributes WHERE attribute_id=%(attribute_id)s AND values=%(value)s",{"attribute_id":searcher.attribute_id,"value":str(searcher.attribute_value)}
        case _:
            query="SELECT asset_id FROM all_atributes WHERE attribute_id=%(attribute_id)s AND values like %(value)s",{"attribute_id":searcher.attribute_id,"value":f"like %{str(searcher.attribute_value)}%"}
    return query
@bp.route("/filter", methods=["POST"])
def filter():
    filter = FilterSearch(**request.json)
    db = get_db()
    filter_asset_ids=[]
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            if filter.tag_operation==QueryOperation.OR:
                cur.execute("""
                SELECT asset_id FROM assets_in_tags WHERE tag_id=ANY(%(tags)s);""",{"tags":filter.tags})
            else:
                cur.execute("""
                SELECT asset_id FROM assets
    WHERE %(tags)s::int[]<@ARRAY(SELECT tag_id FROM assets_in_tags WHERE assets_in_tags.asset_id=assets.asset_id);
                """,{"tags":filter.tags})
            tags_asset_ids = [row["asset_id"] for row in cur.fetchall()]
            filter_asset_ids.append(set(tags_asset_ids))
            if filter.project_operation==QueryOperation.OR:
                cur.execute("""
                SELECT asset_id FROM assets_in_projects WHERE project_id=ANY(%(projects)s);""",{"projects":filter.projects})
            else:
                cur.execute("""
                SELECT asset_id FROM assets
    WHERE %(projects)s::int[]<@ARRAY(SELECT project_id FROM assets_in_projects WHERE assets_in_projects.asset_id=assets.asset_id);
                """,{"projects":filter.projects})
            project_asset_ids = [row["asset_id"] for row in cur.fetchall()]
            filter_asset_ids.append(set(project_asset_ids))
            cur.execute("""
            SELECT DISTINCT asset_id FROM assets WHERE classification=ANY(%(classification)s);
            """,{"classification":filter.classifications})
            classification_asset_ids = [row["asset_id"] for row in cur.fetchall()]
            filter_asset_ids.append(set(classification_asset_ids))
            cur.execute("""
            SELECT DISTINCT asset_id FROM assets WHERE version_id=ANY(%(type)s);
            """,{"type":filter.types})
            type_asset_ids = [row["asset_id"] for row in cur.fetchall()]
            filter_asset_ids.append(set(type_asset_ids))
            cur.execute("""
            CREATE or REPLACE view all_atributes as
SELECT asset_id,
   unnest(array[-1,-2,-3]) AS "attribute_id",
   unnest(array[name, link, description]) AS "values"
FROM assets
UNION ALL 
SELECT * FROM attributes_values;
            """)
            db_conn.commit()
            print(filter.attributes)
            for searcher in filter.attributes:
                print(searcher)
                match searcher.operation:
                    case QueryOperation.EQUALS:
                        cur.execute("SELECT asset_id FROM all_atributes WHERE attribute_id=%(attribute_id)s AND values=%(value)s",{"attribute_id":searcher.attribute_id,"value":str(searcher.attribute_value)})
                    case QueryOperation.HAS:
                        cur.execute("SELECT asset_id FROM all_atributes WHERE attribute_id=%(attribute_id)s",{"attribute_id":searcher.attribute_id})
                    case _:
                        cur.execute("SELECT asset_id FROM all_atributes WHERE attribute_id=%(attribute_id)s AND values like %(value)s",{"attribute_id":searcher.attribute_id,"value":f"%{str(searcher.attribute_value)}%"})
                filter_asset_ids.append(set([row["asset_id"] for row in cur.fetchall()]))
            if filter.operation==QueryOperation.AND:  
                asset_ids=set.intersection(*filter_asset_ids)
            else:
                asset_ids=set(chain.from_iterable(filter_asset_ids))
    return {"data": list(asset_ids)}
@bp.route("/upgrade/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def get_upgrade(id,user_id, access_level):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                        """SELECT MAX(version_id) AS version_id FROM type_version
WHERE type_id in (SELECT type_id FROM type_version
INNER JOIN assets ON assets.version_id=type_version.version_id
WHERE asset_id=%(asset_id)s);""",
                        {"asset_id":id},
                    )
            max_version=cur.fetchone()
            print(max_version)
            cur.execute(
                        """SELECT type_version.version_id FROM type_version
INNER JOIN assets ON assets.version_id=type_version.version_id
WHERE asset_id=%(asset_id)s;""",
                        {"asset_id":id},
                    )
            current_version=cur.fetchone()
            if max_version==current_version:
                return {"msg":"no upgrade needed","data":[],"canUpgrade":False}
        with db_conn.cursor(row_factory=class_row(Attribute_Model)) as cur:
            cur.execute("""SELECT attributes.* FROM attributes_in_types 
            INNER JOIN attributes ON attributes.attribute_id=attributes_in_types.attribute_id
            WHERE type_version=%(type_version)s;""",{"type_version":max_version["version_id"]})
            new_attributes=cur.fetchall()
            cur.execute("""SELECT attributes.* FROM attributes_in_types 
            INNER JOIN attributes ON attributes.attribute_id=attributes_in_types.attribute_id
            WHERE type_version=%(type_version)s;""",{"type_version":current_version["version_id"]})
            old_attributes=cur.fetchall()
            added_attributes=[]
            removed_attributes_names=[]
            for attribute in new_attributes:
                if not attribute in old_attributes:
                    added_attributes.append(attribute.dict(by_alias=True))
            for attribute in old_attributes:
                if not attribute in new_attributes:
                    removed_attributes_names.append(attribute.attribute_name)
            return {"msg":"upgrade needed","data":[added_attributes,removed_attributes_names,max_version["version_id"]],"canUpgrade":True}
def abort_asset_not_exists(db,id):
    with db.connection() as db_conn:
        with db_conn.cursor() as cur:
            cur.execute(
                """SELECT asset_id FROM assets WHERE asset_id=%(id)s AND soft_delete=0;""",
                {"id": id},
            )
            if cur.fetchone() is None:
                res=jsonify({"msg": "Asset doesn't exist",
      
                "data": []
            })
                res.status_code=400
                abort(res)

def insert_comment_to_db(db,comment:Comment,user_id,asset_id):
    return run_query(db,"""INSERT INTO comments(asset_id,account_id,comment)
                 VALUES(%(asset_id)s,%(account_id)s,%(comment)s);""",{"asset_id": asset_id,"account_id":user_id,"comment":comment.comment})

def fetch_asset_comments(db,asset_id):
    return run_query(db,"""
    SELECT comments.*,username FROM comments
INNER JOIN accounts ON accounts.account_id=comments.account_id
    WHERE asset_id=%(asset_id)s ORDER BY datetime;""",{"asset_id": asset_id},return_type=QueryResult.ALL,row_factory=class_row(CommentOut))

def audit_log_event(db,model_id,account_id,object_id,diff_dict,action):
    return run_query(db,"""
                INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
        VALUES (%(model_id)s,%(account_id)s,%(object_id)s,%(diff)s,%(action)s);""",
        {"model_id":model_id,"account_id":account_id,"object_id":object_id,"diff":json.dumps(diff_dict),"action":action})

@bp.route("/comment/<id>", methods=["POST"])
@protected(role=UserRole.USER)
def add_comment(id,user_id, access_level):
    print(request.json)
    comment=model_creator(Comment,"Failed to add comment from the data provided",**request.json)
    print(type(comment))
    db = get_db()
    #TODO:Keep db open
    abort_asset_not_exists(db,id)
    print(db,comment,user_id,id)
    insert_comment_to_db(db,comment,user_id,id)
    audit_log_event(db,Models.ASSETS,user_id,id,{"added":["comment"]},Actions.ADD)
    return {"msg": "Comment added"},200

@bp.route("/comment/<id>", methods=["GET"])
@protected(role=UserRole.USER)
def fetch_comments(id,user_id, access_level):
    db = get_db()
    abort_asset_not_exists(db,id)
    comments=[json.loads(c.json(by_alias=True)) for c in fetch_asset_comments(db,id)]
    return {"msg": "Comments","data":comments},200