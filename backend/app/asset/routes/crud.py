from app.core.utils import protected,run_query,QueryResult
from app.db import DataAccess, UserRole, get_db,Actions,Models
from app.schemas import Asset, Attribute, AssetOut,FilterSearch,QueryOperation,AttributeBase,Project,Log,QueryJoin
from flask import Blueprint, jsonify, request
from psycopg.rows import class_row, dict_row
from pydantic import ValidationError
from itertools import chain
import json
from .. import services,utils
from app.core.utils import model_creator
bp = Blueprint("asset", __name__, url_prefix="/asset")



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
        with db_conn.cursor(row_factory=class_row(Attribute)) as cur:
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
    asset=model_creator(model=Asset,err_msg="Failed to create asset from the data provided",**request.json)
    db = get_db()
    db_asset = asset.dict(exclude={"metadata"})
    utils.check_asset_dependencies(db=db,version_id=asset.version_id,assets=asset.assets)
    utils.check_asset_metatadata(db=db,version_id=asset.version_id,metadata=asset.metadata)
    asset_id =  services.add_asset_to_db(db=db,**db_asset)["asset_id"]
    with db.connection() as conn:
        with conn.cursor() as cur:  
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
    return {"msg": "Added asset", "data": asset_id}, 201


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
    return {"data": selected_projects}, 201

@bp.route("links/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def list_asset_in_assets(id,user_id, access_level):
    db = get_db()
    # get related assets for  an asset and set them to be selected for easy rendering on UI
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(Attribute)) as cur:
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
        with db_conn.cursor(row_factory=class_row(Attribute)) as cur:
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
    services.abort_asset_not_exists(db=db,asset_id=id)
    return {"data":services.get_asset_logs(db,id)}

#TODO:Moves to tags
@bp.route("/tags/summary/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def tags_summary(id, user_id, access_level):
    db = get_db()
    assets_json = []
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(Attribute)) as cur:
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
        with db_conn.cursor(row_factory=class_row(AttributeBase)) as cur:
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
        


@bp.route("/filter", methods=["POST"])
def filter():
    """Finds all assets based on filter criteria.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets ids.
    """
    filter=model_creator(model=FilterSearch,err_msg="Failed to run filter from the data provided",**request.json)
    db = get_db()
    # the list of sets of asset ids to joint
    filter_asset_ids=[]
    
    # filter based on tags
    if filter.tag_operation==QueryJoin.OR:
        tags_results=services.fetch_assets_with_any_links(db,filter.tags,link_table="assets_in_tags",fkey="tag_id")
    else:
        tags_results=services.fetch_assets_with_set_links(db,filter.tags,link_table="assets_in_tags",fkey="tag_id")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",tags_results)))
    
    # filter based on projects
    if filter.project_operation==QueryJoin.OR:
        project_results=services.fetch_assets_with_any_links(db=db,fkeys=filter.projects,link_table="assets_in_projects",fkey="project_id")
    else:
        project_results=services.fetch_assets_with_set_links(db,filter.projects,link_table="assets_in_projects",fkey="project_id")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",project_results)))
    
    # filter based on classification
    classification_results=services.fetch_assets_with_any_values(db=db,values=filter.classifications,attribute="classification")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",classification_results)))
    
    # filter based on type
    type_results=services.fetch_assets_with_any_values(db=db,values=filter.types,attribute="version_id")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",type_results)))
    
    # build a view of asset attributes which can searched
    services.create_all_attributes_view(db=db)

    # holds a list of sets of asset ids based on attribute filters
    filter_attributes_results=[]
    # iterates overs all attributes searchers
    for searcher in filter.attributes:
        # apply filter based on attribute
        filter_results=services.fetch_assets_attribute_filter(db=db,searcher=searcher)
        # unpack results of query to get asset ids and adds to interm results 
        filter_results=set(utils.get_key_from_results("asset_id",filter_results))
        filter_attributes_results.append(filter_results)
    print(filter_attributes_results)

    # join interm results  of the the attribute filter
    if filter.attribute_operation==QueryJoin.OR:
        filter_attributes_results=set(chain.from_iterable(filter_attributes_results))
        print("Hello",filter_attributes_results)
    else:
        filter_attributes_results=set.intersection(*filter_attributes_results)
    filter_asset_ids.append(filter_attributes_results)
    
    print(filter_asset_ids)
    # join all interm results based on previous searches
    if filter.operation==QueryJoin.AND:  
        asset_ids=set.intersection(*filter_asset_ids)
    else:
        asset_ids=set(chain.from_iterable(filter_asset_ids))
    return {"data": list(asset_ids)}

