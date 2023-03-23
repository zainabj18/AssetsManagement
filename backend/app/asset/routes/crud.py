from app.core.utils import protected,audit_log_event
from app.db import DataAccess, UserRole, get_db,Actions,Models
from app.schemas import Asset
from flask import Blueprint, request
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
    asset_id=utils.add_asset_to_db(db=db,data=request.json,account_id=user_id)
    audit_log_event(db,Models.ASSETS,user_id,asset_id,{"added":list(Asset.schema(by_alias=True)["properties"].keys())},Actions.ADD)
    return {"msg": "Added asset", "data": asset_id}, 201

@bp.route("/classifications", methods=["GET"])
@protected(role=UserRole.VIEWER)
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

@bp.route("/my", methods=["GET"])
@protected(role=UserRole.VIEWER)
def my_assets(user_id, access_level):
    db = get_db()
    return {"data": services.fetch_assets_summary(db=db,classification=access_level,account_id=user_id)}

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
    utils.add_asset_to_db(db=db,data=request.json,asset_id=id,account_id=user_id)
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
    if dependencies:
        return {"msg":"Asset has dependencies","data":dependencies}, 400
    services.delete_tags_from_asset(db=db,asset_id=id)
    services.delete_projects_from_asset(db=db,asset_id=id)
    services.delete_assets_from_asset(db=db,asset_id=id)
    services.delete_attributes_from_asset(db=db,asset_id=id)
    services.delete_asset(db=db,asset_id=id)
    audit_log_event(db,Models.ASSETS,user_id,id,{},Actions.DELETE)
    return {}, 200
