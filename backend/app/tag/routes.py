from app.db import get_db, UserRole,Actions,Models
from app.schemas import TagBase,TagBulkRequest
from app.core.utils import protected,model_creator,audit_log_event
from flask import Blueprint, jsonify, request
from . import services

bp = Blueprint("tag", __name__, url_prefix="/tag")


@bp.route("/", methods=["POST"])
@protected(role=UserRole.USER)
def create(user_id, access_level):
    tag=model_creator(model=TagBase,err_msg="Failed to create tag from the data provided",**request.json)
    db = get_db()
    
    id=services.insert_tag_to_db(db=db,tag=tag)["id"]
    tag.id = id
    audit_log_event(db,Models.TAGS,user_id,id,{},Actions.ADD)
    return jsonify({"msg": "Tag Created", "data": tag.dict()})


@bp.route("/", methods=["GET"])
@protected(role=UserRole.VIEWER)
def list(user_id, access_level):
    db = get_db()
    tags = services.list_tags(db)
    return {"msg": "tags", "data": tags}




@bp.route("/<id>", methods=["DELETE"])
@protected(role=UserRole.USER)
def delete(id, user_id, access_level):
    db = get_db()
    services.tag_in_db(db=db,tag_id=id)
    services.delete_tag(db, id)
    audit_log_event(db,Models.TAGS,user_id,id,{},Actions.DELETE)
    return {}, 200




@bp.route("/<id>", methods=["PATCH"])
@protected(role=UserRole.ADMIN)
def update(id, user_id, access_level):
    db = get_db()
    services.tag_in_db(db=db,tag_id=id)
    tag=model_creator(model=TagBase,err_msg="Failed to create tag from the data provided",**request.json)
    tag.id = id
    services.update_tag(db=db,tag=tag)
    audit_log_event(db,Models.TAGS,user_id,id,{},Actions.CHANGE)
    return {"msg": "Tag Updated"}, 200

@bp.route("/copy", methods=["POST"])
@protected(role=UserRole.USER)
def copy(user_id, access_level):
    tag_copy=model_creator(model=TagBulkRequest,err_msg="Failed to copy to tag from the data provided",**request.json)
    db=get_db()
    if not services.tag_in_db(db,tag_copy.to_tag_id,abort=False):
        return {"msg": f"Tag {tag_copy.to_tag_id} doesn't exist"},400
    services.add_asset_to_tag(db=db,asset_ids=tag_copy.assest_ids,tag_id=tag_copy.to_tag_id)
    for id in tag_copy.assest_ids:
        audit_log_event(db,Models.ASSETS,user_id,id,{"changed":[["tag_ids",[],[tag_copy.to_tag_id]]]},Actions.CHANGE)
    return {"msg":"Copied assets to tag"}, 200

"""_summary_
 Parameters:
    id : The ID all the assets that belong to the same project .
    Returns:
        json data
"""
@bp.route("/remove", methods=["POST"])
@protected(role=UserRole.USER)
def remove(user_id, access_level):
    tag_remove=model_creator(model=TagBulkRequest,err_msg="Failed to remove to tag from the data provided",**request.json)
    db=get_db()
    if not services.tag_in_db(db,tag_remove.to_tag_id,abort=False):
        return {"msg": f"Tag {tag_remove.to_tag_id} doesn't exist"},400
    services.delete_asset_in_tag(db,tag_remove.assest_ids,tag_remove.to_tag_id)
    for id in tag_remove.assest_ids:
        audit_log_event(db,Models.ASSETS,user_id,id,{"changed":[["tagIDs",[tag_remove.to_tag_id],[]]]},Actions.CHANGE)
    return {"msg":"Removed assets from tag"}, 200

@bp.route("/assets/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def tags_summary(id, user_id, access_level):
    """
    Gets all assets in a tag
    """
    db = get_db()
    services.tag_in_db(db=db,tag_id=id)
    tag_name=services.fetch_tag_name(db=db,tag_id=id)
    assets=services.fetch_assets_in_tag(db=db,tag_id=id)
    res = jsonify({"data": {"tag":tag_name , "assets":assets}})
    return res

