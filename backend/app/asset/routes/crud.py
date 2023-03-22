from app.core.utils import protected,run_query,QueryResult,audit_log_event
from app.db import DataAccess, UserRole, get_db,Actions,Models
from app.schemas import Asset, Attribute, AssetOut,FilterSearch,QueryOperation,AttributeBase,Project,Log,QueryJoin,AssetBaseInDB
from flask import Blueprint, jsonify, request
from psycopg.rows import class_row, dict_row
import json
from .. import services,utils
from app.core.utils import model_creator
bp = Blueprint("asset", __name__, url_prefix="/asset")

@bp.route("/", methods=["POST"])
@protected(role=UserRole.USER)
def create(user_id, access_level):
    """Add a new asset to the db.

    Args:
      user_id: The id of the user making the request.
      access_level: The access_level of the user.
    
    Returns:
      A msg saying asset added.
    """
    db = get_db()
    asset_id=utils.add_asset_to_db(db=db,data=request.json)
    audit_log_event(db,Models.ASSETS,user_id,asset_id,{"added":list(Asset.schema(by_alias=True)["properties"].keys())},Actions.ADD)
    return {"msg": "Added asset", "data": asset_id}, 201

@bp.route("/classifications", methods=["GET"])
@protected(role=UserRole.USER)
def get_classifications(user_id, access_level):
    """Gets all classifications from db.

    Args:
      user_id: The id of the user making the request.
      access_level: The access_level of the user.
    
    Returns:
      A list of classifications that the user can view
    """
    viwable_classifications = []
    for c in DataAccess:
        if c <= access_level:
            viwable_classifications.append(c.value)
    return {"data": viwable_classifications}

@bp.route("/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def view(id, user_id, access_level):
    db = get_db()
    utils.can_view_asset(db=db,asset_id=id,access_level=access_level)
    asset=services.fetch_asset(db,id)
    return {"data": json.loads(asset.json(by_alias=True))}

@bp.route("/summary", methods=["GET"])
@protected(role=UserRole.VIEWER)
def summary(user_id, access_level):
    db = get_db()
    return {"data": services.fetch_assets_summary(db=db,classification=access_level)}

@bp.route("projects/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def list_asset_project(id,user_id, access_level):
    db = get_db()
    utils.can_view_asset(db=db,asset_id=id,access_level=access_level)
    projects=services.fetch_assets_projects_selected(db=db,asset_id=id)
    return {"data": projects}

@bp.route("links/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def list_asset_links(id,user_id, access_level):
    db = get_db()
    utils.can_view_asset(db=db,asset_id=id,access_level=access_level)
    assets=services.fetch_assets_asssets_selected(db=db,asset_id=id,classification=access_level)
    return {"data": assets}

@bp.route("/upgrade/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def get_upgrade(id,user_id, access_level):
    db = get_db()
    utils.can_view_asset(db=db,asset_id=id,access_level=access_level)
    results=services.fetch_asset_current_and_max_versions(db=db,asset_id=id)
    if results["version_id"]==results["max_version_id"]:
        return {"msg":"no upgrade needed","data":[]}
    new_attributes=services.fetch_versions_attributes(db=db,version_id=results["max_version_id"])
    old_attributes=services.fetch_versions_attributes(db=db,version_id=results["version_id"])
    new_dependencies=services.fetch_version_dependencies(db=db,version_id=results["max_version_id"])
    new_dependencies_names=[depdencent["type_name"] for depdencent in new_dependencies]
    added_attributes=[]
    removed_attributes_names=[]
    for attribute in new_attributes:
        if not attribute in old_attributes:
            added_attributes.append(attribute)
    for attribute in old_attributes:
        if not attribute in new_attributes:
            removed_attributes_names.append(attribute["attributeName"])
    return {"msg":"upgrade needed","data":{"addedAttributes":added_attributes,"removedAttributesNames":removed_attributes_names,"dependsOn":new_dependencies_names,"maxVersion":results["max_version_id"]}}

@bp.route("/<id>", methods=["PATCH"])
@protected(role=UserRole.VIEWER)
def update(id, user_id, access_level):
    db = get_db()
    utils.can_view_asset(db=db,asset_id=id,access_level=access_level)
    new_asset=model_creator(model=Asset,err_msg="Failed to create asset from the data provided",**request.json)
    old_asset=Asset(**services.fetch_asset_flattend(db=db,asset_id=id).dict())
    diff=utils.asset_differ(old_asset.dict(by_alias=True),new_asset.dict(by_alias=True))
    utils.add_asset_to_db(db=db,data=request.json,asset_id=id)
    tags_removed=list(set(old_asset.tag_ids)-set(new_asset.tag_ids))
    projects_removed=list(set(old_asset.project_ids)-set(new_asset.project_ids))
    assets_removed=list(set(old_asset.asset_ids)-set(new_asset.asset_ids))
    attributes_removed=list(set([a.attribute_id for a in old_asset.metadata])-set([a.attribute_id for a in new_asset.metadata]))
    services.delete_tags_from_asset(db=db,asset_id=id,tags=tags_removed)
    services.delete_projects_from_asset(db=db,asset_id=id,projects=projects_removed)
    services.delete_assets_from_asset(db=db,asset_id=id,asset_ids=assets_removed)
    services.delete_attributes_from_asset(db=db,asset_id=id,attributes=attributes_removed)
    audit_log_event(db,Models.ASSETS,user_id,id,diff,Actions.CHANGE)
    return {"msg": "Updated asset"}


@bp.route("/<id>", methods=["DELETE"])
@protected(role=UserRole.USER)
def delete(id,user_id, access_level):
    db = get_db()
    utils.can_view_asset(db=db,asset_id=id,access_level=access_level)
    dependencies=services.fetch_asset_dependencies(db=db,asset_id=id)
    print(dependencies)
    if dependencies:
        return {"msg":"Asset has dependencies","data":dependencies}, 400
    services.delete_tags_from_asset(db=db,asset_id=id)
    services.delete_projects_from_asset(db=db,asset_id=id)
    services.delete_assets_from_asset(db=db,asset_id=id)
    services.delete_attributes_from_asset(db=db,asset_id=id)
    services.delete_asset(db=db,asset_id=id)
    #TODO:Abort if can't view

    return {}, 200

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

