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
    query = """INSERT INTO attributes (attribute_name, attribute_data_type) VALUES (%(attribute_name)s, %(attribute_type)s);"""
    with database.connection() as conn:
        conn.execute(query, db_attribute)
    return {"msg": ""}, 200


@bp.route("/<id>", methods=["POST"])
def get_type(id):
    database = get_db()
    query = """SELECT type_name, attribute_name, attribute_data_type FROM attributes_in_types AS at INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id INNER JOIN types AS t on at.type_id = t.type_id WHERE t.type_id = (%(id)s);"""
    with database.connection() as conn:
        res = conn.execute(query, {"id": id})
        type = res.fetchone()
        return json.dumps({
            "typeName": type[0],
            "metadata": [
                {
                    "attributeName": type[1],
                    "attributeType": type[2]
                }
            ]
        }), 200


def extract_attributes(attributes):
    allAttributes_listed = []
    for attribute in attributes:
        allAttributes_listed.append({
            "attributeName": attribute[0],
            "attributeType": attribute[1]
        })
    return allAttributes_listed


@bp.route("/allAttributes", methods=["POST"])
def get_allAttributes():
    database = get_db()
    query = """SELECT attribute_name, attribute_data_type FROM attributes;"""
    with database.connection() as conn:
        res = conn.execute(query)
        allAttributes = res.fetchall()
        allAttributes_listed = extract_attributes(allAttributes)
        return json.dumps({"attributes": allAttributes_listed})


@bp.route("/allTypes", methods=["GET"])
def get_allTypes():
    database = get_db()
    query_a = """SELECT type_id, type_name FROM types;"""
    with database.connection() as conn:
        res = conn.execute(query_a)
        allTypes = res.fetchall()
        allTypes_listed = []
        for type in allTypes:
            query_b = """SELECT attribute_name, attribute_data_type FROM attributes_in_types AS at INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id INNER JOIN types AS t on at.type_id = t.type_id WHERE t.type_id = %(type_id)s;"""
            res = conn.execute(query_b, {"type_id": type[0]})
            attributes = extract_attributes(res.fetchall())
            allTypes_listed.append({
                "typeId": type[0],
                "typeName": type[1],
                "metadata": attributes
            })
        return json.dumps(allTypes_listed), 200
