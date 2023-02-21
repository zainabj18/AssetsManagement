from app.core.utils import protected
from app.db import DataAccess, UserRole, get_db
from app.schemas import Asset, AssetBaseInDB, AssetOut, AttributeInDB
from flask import Blueprint, jsonify, request
from psycopg.rows import class_row, dict_row
from pydantic import ValidationError

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
                """SELECT attributes.attribute_id,attribute_name, attribute_data_type as attribute_type, validation_data,value as attribute_value FROM attributes_values 
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
            projects = cur.fetchall()
            cur.execute(
                """SELECT tags.id,name FROM assets_in_tags 
INNER JOIN tags on tags.id=assets_in_tags.tag_id WHERE asset_id=%(id)s;""",
                {"id": id},
            )
            tags = list(cur.fetchall())
            cur.execute(
                """SELECT type_name FROM types WHERE type_id=%(id)s;""",
                {"id": asset.type},
            )
            type = cur.fetchone()["type_name"]

        asset = AssetOut(
            **asset.dict(), metadata=metadata, projects=projects, tags=tags
        )
        asset.type = type
    return asset
@bp.route("/", methods=["POST"])
def create():
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
    # add asset to db
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO assets (name,link,type,description, classification)
    VALUES (%(name)s,%(link)s,%(type)s,%(description)s,%(classification)s)  RETURNING asset_id;""",
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
            selected_projects = list(cur.fetchall())
            print(selected_projects)
            for x in selected_projects:
                x["isSelected"] = True
            cur.execute(
                """SELECT * FROM projects WHERE id not in (SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s);""",
                {"id": id},
            )
            projects = list(cur.fetchall())
            selected_projects.extend(projects)
    return {"data": selected_projects}, 200


@bp.route("/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def view(id, user_id, access_level):
    db = get_db()
    asset=fetch_asset(db,id,access_level)
    
    return {"data": json.loads(asset.json(by_alias=True))}, 200


@bp.route("/<id>", methods=["DELETE"])
def delete(id):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
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
            cur.execute("""SELECT * FROM assets WHERE soft_delete=0;""")
            assets = cur.fetchall()
        # gets the type name for each assset
        with db_conn.cursor(row_factory=dict_row) as cur:
            for a in assets:
                if a.classification <= access_level:
                    cur.execute(
                        """SELECT type_name FROM types WHERE type_id=%(id)s;""",
                        {"id": a.type},
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
    orgignal_asset["projects"]=[project["id"]for project in orgignal_asset["projects"]]
    projects_removed=list(set(orgignal_asset["projects"])-set(asset["projects"]))
    projects_added=list(set(asset["projects"])-set(orgignal_asset["projects"]))
    tags_removed=list(set(orgignal_asset["tags"])-set(asset["tags"]))
    tags_added=list(set(asset["tags"])-set(orgignal_asset["tags"]))

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            UPDATE assets 
            SET name=%(name)s,link=%(link)s,description=%(description)s,classification=%(classification)s,last_modified_at=now() WHERE asset_id=%(asset_id)s ;""",
                asset,
            )
            cur.execute("""
            DELETE FROM assets_in_tags WHERE tag_id = ANY(%(tag_ids)s) AND asset_id=%(asset_id)s;
            """,{"tag_ids":tags_removed,"asset_id":asset["asset_id"]})
            cur.execute("""
            DELETE FROM assets_in_projects WHERE project_id = ANY(%(project_ids)s) AND asset_id=%(asset_id)s;
            """,{"project_ids":projects_removed,"asset_id":asset["asset_id"]})
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
            for attribute in asset["metadata"]:
                cur.execute(
                    """
                UPDATE attributes_values 
                SET value=%(attributeValue)s WHERE asset_id=%(asset_id)s AND attribute_id=%(attributeID)s;""",
                    {"asset_id": id, **attribute},
                )
            
    return {}, 200


@bp.route("/tags/summary/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def tags_summary(id, user_id, access_level):
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(
                """SELECT assets.* FROM assets
INNER JOIN assets_in_tags ON assets.asset_id=assets_in_tags.asset_id WHERE soft_delete=0 AND tag_id=%(tag_id)s;""",
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
                        """SELECT type_name FROM types WHERE type_id=%(id)s;""",
                        {"id": a.type},
                    )
                    type = cur.fetchone()["type_name"]
                    aj = json.loads(a.json(by_alias=True))
                    aj["type"] = type
                    assets_json.append(aj)
            res = jsonify({"data": {"tag": tag, "assets": assets_json}})
    return res
