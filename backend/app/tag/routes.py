from flask import Blueprint, jsonify, request
from app.db import get_db
from pydantic import ValidationError
from app.schemas import TagBase

bp = Blueprint("tag", __name__, url_prefix="/tag")

def create_tag(db,tag_dict):
    with db.connection() as conn:
         with conn.cursor() as cur:
            cur.execute(
            """
        INSERT INTO tags (name)
VALUES (%(name)s) RETURNING id;""",
            tag_dict,
        )
            return cur.fetchone()[0]

@bp.route("/", methods=["POST"])
def create():
    try:
       tag=TagBase(**request.json)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": e.errors(),
                    "error": "Failed to create tag from the data provided",
                }
            ),
            400,
        )
    db = get_db()
    id=create_tag(db,tag.dict())
    tag.id=id
    return jsonify({"msg": "Tag Created","data":tag.dict()})