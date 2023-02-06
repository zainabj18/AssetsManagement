import json
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

    query = """INSERT INTO attributes_in_types (attribute_id, type_id) VALUES ((SELECT attribute_id FROM attributes WHERE attribute_name = (%(attr_name)s)), (SELECT type_id FROM types WHERE type_name = (%(type_name)s)))"""
    for attribute in new_type.metadata:
        with database.connection() as conn:
            conn.execute(query, {"type_name": new_type.type_name,
                         "attr_name": attribute.attribute_name})

    return {"msg": ""}, 200


@bp.route("/adder", methods=["GET"])
def types():
    return {"msg": ""}, 200


@bp.route("/adder/new", methods=["POST"])
def add_attribute():
    new_attribute = Attribute_Model(**request.json)
    db_attribute = new_attribute.dict()
    database = get_db()
    query = """INSERT INTO ATTRIBUTES (attribute_name, attribute_data_type) VALUES (%(attribute_name)s, %(attribute_type)s);"""
    with database.connection() as conn:
        conn.execute(query, db_attribute)
    return {"msg": ""}, 200
