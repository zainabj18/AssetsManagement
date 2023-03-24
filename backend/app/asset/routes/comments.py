from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint, request

from app.core.utils import audit_log_event, model_creator, protected
from app.db import Actions, DataAccess, Models, UserRole, get_db
from app.schemas import Comment, CommentOut

from ..services import delete_comment_db, fetch_asset_comments, insert_comment_to_db
from ..utils import can_view_asset

bp = Blueprint("comment", __name__, url_prefix="/comment")


@bp.route("/<id>", methods=["POST"])
@protected(role=UserRole.USER)
@swag_from(
    {
        "parameters": [{"name": "id", "in": "path", "type": "int"}],
        "responses": {HTTPStatus.OK.value: {"description": "successful operation"}},
    }
)
def add_comment(id: int, user_id: int, access_level: DataAccess):
    """Add a new comment to the db.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access_level of the user.

    Returns:
      A msg saying comment added.
    """
    comment = model_creator(
        model=Comment,
        err_msg="Failed to add comment from the data provided",
        **request.json,
    )
    db = get_db()
    can_view_asset(db=db, asset_id=id, access_level=access_level)
    insert_comment_to_db(db, comment, user_id, id)
    audit_log_event(db, Models.ASSETS, user_id, id, {"added": ["comment"]}, Actions.ADD)
    return {"msg": "Comment added"}


@bp.route("/<id>", methods=["GET"])
@protected(role=UserRole.USER)
@swag_from(
    {
        "parameters": [{"name": "id", "in": "path", "type": "int"}],
        "responses": {
            HTTPStatus.OK.value: {
                "description": "Get comments in db.",
                "schema": {"type": "array", "items": CommentOut.schema(by_alias=True)},
            }
        },
    }
)
def fetch_comments(id: int, user_id: int, access_level: DataAccess):
    """Find all comments related to an asset.

    Args:
      id: The asset id to search for related comments.
      user_id: The id of the user making the request.
      access_level: The access_level of the user.

    Returns:
      A list of comments as dicts for an asset.
    """
    db = get_db()
    can_view_asset(db=db, asset_id=id, access_level=access_level)
    comments = fetch_asset_comments(db, id)
    return {"msg": "Comments", "data": comments}


@bp.route("/<id>/remove/<comment_id>", methods=["DELETE"])
@protected(role=UserRole.ADMIN)
@swag_from(
    {
        "parameters": [
            {"name": "id", "in": "path", "type": "int"},
            {"name": "comment_id", "in": "path", "type": "int"},
        ],
        "responses": {HTTPStatus.OK.value: {"description": "successful operation"}},
    }
)
def delete_comment(id: int, comment_id: int, user_id: int, access_level: DataAccess):
    """Delete a comments related to an asset.

    Args:
      id: The asset id to search for related comments.
      comment_id: The comment id to delete from asset.
      user_id: The id of the user making the request.
      access_level: The access_level of the user.

    Returns:
      A msg saying it has been deleted.
    """
    db = get_db()
    can_view_asset(db=db, asset_id=id, access_level=access_level)
    delete_comment_db(db, comment_id)
    audit_log_event(
        db,
        Models.ASSETS,
        user_id,
        id,
        {"removed": [f"comment-{comment_id}"]},
        Actions.ADD,
    )
    return {"msg": "Comment deleted"}
