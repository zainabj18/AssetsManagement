
from flask import Blueprint,request
from .services import abort_asset_not_exists,insert_comment_to_db,fetch_asset_comments,delete_comment_db
from app.core.utils import protected,run_query,model_creator,QueryResult,audit_log_event
from app.db import UserRole, get_db,Actions,Models
from app.schemas import Comment,CommentOut
from psycopg.rows import class_row
bp = Blueprint("comment", __name__, url_prefix="/comment")


@bp.route("/<id>", methods=["POST"])
@protected(role=UserRole.USER)
def add_comment(id,user_id, access_level):
    comment=model_creator(model=Comment,err_msg="Failed to add comment from the data provided",**request.json)
    db = get_db()
    abort_asset_not_exists(db,id)
    insert_comment_to_db(db,comment,user_id,id)
    audit_log_event(db,Models.ASSETS,user_id,id,{"added":["comment"]},Actions.ADD)
    return {"msg": "Comment added"}

@bp.route("/<id>", methods=["GET"])
@protected(role=UserRole.USER)
def fetch_comments(id,user_id, access_level):
    db = get_db()
    abort_asset_not_exists(db,id)
    comments=fetch_asset_comments(db,id)
    return {"msg": "Comments","data":comments}

@bp.route("/<id>/remove/<comment_id>", methods=["DELETE"])
@protected(role=UserRole.ADMIN)
def delete_comment(id,comment_id,user_id, access_level):
    db = get_db()
    delete_comment_db(db,comment_id)
    audit_log_event(db,Models.ASSETS,user_id,id,{"removed":[f"comment-{comment_id}"]},Actions.ADD)
    return {"msg": "Comment deleted"}