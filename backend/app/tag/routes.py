from app.db import get_db, UserRole,Actions
from app.schemas import TagBase,TagBulkRequest
from app.core.utils import protected
from flask import Blueprint, jsonify, request
from psycopg import Error
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row
from pydantic import ValidationError
import json

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

def update_tag(db,tag_dict):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            UPDATE tags 
            SET name=%(name)s WHERE id=%(id)s ;""",
                tag_dict,
            )

def add_asset_to_tag(db,asset_ids,tag_id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO assets_in_tags(asset_id,tag_id)
SELECT asset_id,%(tag_id)s AS tag_id FROM assets
WHERE asset_id = ANY(%(asset_ids)s) ON CONFLICT DO NOTHING;
            """,{"tag_id":tag_id,"asset_ids":asset_ids})

def delete_asset_in_tag(db,asset_ids,tag_id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM assets_in_tags WHERE asset_id = ANY(%(asset_ids)s) AND tag_id=%(tag_id)s;
            """,{"tag_id":tag_id,"asset_ids":asset_ids})



def list_tags(db):
    with db.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM tags ORDER BY name;""")
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

"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""


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
    with db.connection() as db_conn:
        with db_conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
        VALUES (4,%(account_id)s,%(tag_id)s,%(diff)s,%(action)s);""",
                {"account_id":user_id,"tag_id":id,"diff":json.dumps({}),"action":Actions.ADD},
            )
    return jsonify({"msg": "Tag Created", "data": tag.dict()})
"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""


@bp.route("/", methods=["GET"])
@protected(role=UserRole.VIEWER)
def list(user_id, access_level):
    try:
        db = get_db()
        tags = list_tags(db)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return jsonify({"msg": "tags", "data": tags})

"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""


@bp.route("/<id>", methods=["DELETE"])
@protected(role=UserRole.USER)
def delete(id, user_id, access_level):
    try:
        db = get_db()
        delete_tag(db, id)
        with db.connection() as db_conn:
            with db_conn.cursor() as cur:
                cur.execute(
                    """
                INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
            VALUES (4,%(account_id)s,%(tag_id)s,%(diff)s,%(action)s);""",
                    {"account_id":user_id,"tag_id":id,"diff":json.dumps({}),"action":Actions.DELETE},
                )
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return {}, 200

"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""


@bp.route("/<id>", methods=["PATCH"])
@protected(role=UserRole.ADMIN)
def update(id, user_id, access_level):
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
    try:
        db = get_db()
        update_tag(db,tag.dict())
        with db.connection() as db_conn:
            with db_conn.cursor() as cur:
                cur.execute(
                    """
                INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
            VALUES (4,%(account_id)s,%(tag_id)s,%(diff)s,%(action)s);""",
                    {"account_id":user_id,"tag_id":id,"diff":json.dumps({}),"action":Actions.CHANGE},
                )
        
    except UniqueViolation as e:
        return {"msg": f"Tag {tag.name} already exists", "error": "Database Error"}, 500
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return {}, 200

@bp.route("/copy", methods=["POST"])
@protected(role=UserRole.USER)
def copy(user_id, access_level):
    try:
        tag_copy = TagBulkRequest(**request.json)
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


@bp.route("/remove", methods=["POST"])
@protected(role=UserRole.USER)
def remove(user_id, access_level):
    try:
        tag_remove = TagBulkRequest(**request.json)
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
    try:
        db=get_db()
        if not tag_in_db(db,tag_remove.to_tag_id):
            return {"msg": "Data provided is invalid","data":tag_remove.to_tag_id,"error": f"Tag {tag_remove.to_tag_id} doesn't exist"},400
        delete_asset_in_tag(db,tag_remove.assest_ids,tag_remove.to_tag_id)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return {"msg":"Removed assets from tag"}, 200