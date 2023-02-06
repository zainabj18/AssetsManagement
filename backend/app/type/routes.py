from flask import Blueprint, request

from app.db import get_db
from app.schemas import Attribute_Model, Type

bp = Blueprint("type", __name__, url_prefix="/type")

@bp.route("/new", methods=["POST"])
def add_type():
    new_type = Type(**request.json)
    db_type = new_type.dict(exclude={"metadata"})
    query = """INSERT INTO types (type_name) VALUES (%(type_name)s);"""
    database = get_db()
    with database.connection() as conn:
        conn.execute(query, db_type)
    return {"msg": ""}, 200


@bp.route("/adder", methods=["GET"])
def types():
    return {"msg": ""}, 200

@bp.route("/adder/new", methods=["POST"])
def add_attribute():
    new_attibute = Attribute_Model(**request.json)
    db_attribute = new_attibute.dict()
    query = """INSERT INTO ATTRIBUTES (attribute_name, attribute_data_type) VALUES (%(attribute_name)s, %(attribute_type)s);"""
    database = get_db()
    with database.connection() as conn:
        conn.execute(query, db_attribute)
    return {"msg": ""}, 200
