from app.db import get_db, UserRole
from app.schemas import TagBase,TagCopy,TagMove
from app.core.utils import protected
from flask import Blueprint, jsonify, request
from psycopg import Error
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row
from pydantic import ValidationError

bp = Blueprint("tag", __name__, url_prefix="/tag")


def create_tag(db, tag_dict):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
        INSERT INTO tags (name)
VALUES (%(name)s) RETURNING id;""",
                tag_dict,
            )
            return cur.fetchone()[0]

def add_asset_to_tag(db,asset_ids,tag_id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO assets_in_tags(asset_id,tag_id)
SELECT asset_id,%(tag_id)s AS tag_id FROM assets
WHERE asset_id = ANY(%(asset_ids)s) ON CONFLICT DO NOTHING;
            """,{"tag_id":tag_id,"asset_ids":asset_ids})



def list_tags(db):
    with db.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM tags;""")
            return cur.fetchall()

def tag_in_db(db,id):
    with db.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT id FROM tags WHERE id=%(id)s;""",{"id": id})
            return cur.fetchall()!=[]


def delete_tag(db, id):
    with db.connection() as db_conn:
        with db_conn.cursor() as cur:
            cur.execute(
                """DELETE FROM tags WHERE id=%(id)s;""",
                {"id": id},
            )


@bp.route("/", methods=["POST"])
@protected(role=UserRole.USER)
def create(user_id, access_level):
    try:
        tag = TagBase(**request.json)
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
    try:
        id = create_tag(db, tag.dict())
    except UniqueViolation as e:
        return {"msg": f"Tag {tag.name} already exists", "error": "Database Error"}, 500
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    tag.id = id
    return jsonify({"msg": "Tag Created", "data": tag.dict()})


@bp.route("/", methods=["GET"])
@protected(role=UserRole.VIEWER)
def list(user_id, access_level):
    try:
        db = get_db()
        tags = list_tags(db)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return jsonify({"msg": "tags", "data": tags})


@bp.route("/<id>", methods=["DELETE"])
@protected(role=UserRole.USER)
def delete(id, user_id, access_level):
    try:
        db = get_db()
        delete_tag(db, id)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return {}, 200

@bp.route("/copy", methods=["POST"])
@protected(role=UserRole.USER)
def copy(user_id, access_level):
    try:
        tag_copy = TagCopy(**request.json)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": e.errors(),
                    "error": "Failed to copy to tag from the data provided",
                }
            ),
            400,
        )
    try:
        db=get_db()
        if not tag_in_db(db,tag_copy.to_tag_id):
            return {"msg": "Data provided is invalid","data":tag_copy.to_tag_id,"error": f"Tag {tag_copy.to_tag_id} doesn't exist"},400
        add_asset_to_tag(db=db,asset_ids=tag_copy.assest_ids,tag_id=tag_copy.to_tag_id)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return {"msg":"Copied assets to tag"}, 200


@bp.route("/move", methods=["POST"])
def move():
    try:
        tag_move = TagMove(**request.json)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": e.errors(),
                    "error": "Failed to move to tag from the data provided",
                }
            ),
            400,
        )
    db=get_db()
    for tag in [tag_move.to_tag_id,tag_move.from_tag_id]:
        if not tag_in_db(db,tag):
            return {"msg": "Data provided is invalid","data":tag,"error": f"Tag {tag} doesn't exist"},400