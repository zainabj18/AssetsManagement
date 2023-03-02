import json

from app.db import get_db
from app.schemas import Attribute_Model, Type
from flask import Blueprint, request
from psycopg.rows import dict_row


def make_query(db, query, params):
    with db.connection() as conn:
        result = conn.execute(query, params)
        return result


def get_types(db):
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM types;""")
            return cur.fetchall()


bp = Blueprint("type", __name__, url_prefix="/type")


@bp.route("/new", methods=["POST"])
def add_type():
    new_type = Type(**request.json)
    db_type = new_type.dict(exclude={"metadata", "depends_on"})
    database = get_db()

    query = """
    SELECT version_number FROM type_version
    INNER JOIN types ON types.type_id = type_version.type_id
    WHERE type_name = %(type_name)s;
    """
    result = make_query(database, query, db_type)
    type_version_number = 1
    if result.fetchone() != None:
        type_version_number = result.fetchone()[0] + 1

    if type_version_number == 1:
        query = """INSERT INTO types (type_name) VALUES (%(type_name)s) RETURNING type_id;"""
    else:
        query = """SELECT type_id FROM types WHERE type_nmae = %(type_name)s"""

    type_id = make_query(database, query, db_type).fetchone()[0]

    query = """
    INSERT INTO type_version (version_number, type_id)
    VALUES (%(version_number)s,%(type_id)s)
    RETURNING version_id;
    """
    params = {"version_number": type_version_number, "type_id": type_id}
    type_version = make_query(database, query, params).fetchone()[0]

    query = """
    INSERT INTO attributes_in_types (attribute_id, type_version)
    VALUES (%(attr_id)s, %(type_version)s)
    """
    for attribute in new_type.metadata:
        params = {"type_version": type_version,
                  "attr_id": attribute.attribute_id}
        make_query(database, query, params)

    query = """
    INSERT INTO type_version_link (type_version_from, type_version_to)
    VALUES (%(from)s, %(to)s)
    """
    selfDependent_error = False
    for dependency_key in new_type.depends_on:
        # If the id refers to itself, it is skipped and an error code will be returned
        # Though the rest of the dependecies will still be added
        if type_id != dependency_key:
            params = {"from": type_version, "to": dependency_key}
            make_query(database, query, params)
        else:
            selfDependent_error = True

    if selfDependent_error:
        return {"msg": "Type can not depend on self"}, 422
    else:
        return {"msg": ""}, 200


@bp.route("/names", methods=["GET"])
def list():
    db = get_db()
    return {"msg": "types", "data": get_types(db)}, 200


@bp.route("/adder/new", methods=["POST"])
def add_attribute():
    new_attribute = Attribute_Model(**request.json)
    db_attribute = new_attribute.dict(exclude={"validation_data"})
    db_attribute["validation_data"] = json.dumps(new_attribute.validation_data)
    database = get_db()
    query = """INSERT INTO attributes (attribute_name, attribute_data_type, validation_data) VALUES (%(attribute_name)s, %(attribute_type)s, %(validation_data)s);"""
    with database.connection() as conn:
        conn.execute(query, db_attribute)
    return {"msg": ""}, 200


@bp.route("/<id>", methods=["GET"])
def get_type(id):
    database = get_db()
    query_a = """SELECT type_id, type_name FROM types;"""
    with database.connection() as conn:
        res = conn.execute(query_a)
        type = res.fetchone()
        query_b = """SELECT at.attribute_id,attribute_name, attribute_data_type, validation_data FROM attributes_in_types AS at INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id INNER JOIN types AS t on at.type_id = t.type_id WHERE t.type_id = %(type_id)s;"""
        res = conn.execute(query_b, {"type_id": id})
        attributes = extract_attributes(res.fetchall())
        return {"typeId": type[0], "typeName": type[1], "metadata": attributes}, 200


def extract_attributes(attributes):
    allAttributes_listed = []
    for attribute in attributes:

        if attribute[2] == None:
            allAttributes_listed.append(
                {
                    "attributeID": attribute[0],
                    "attributeName": attribute[1],
                    "attributeType": attribute[3],
                }
            )
        else:
            allAttributes_listed.append(
                {
                    "attributeID": attribute[0],
                    "attributeName": attribute[1],
                    "attributeType": attribute[2],
                    "validation": attribute[3],
                }
            )
    return allAttributes_listed


@bp.route("/allAttributes", methods=["GET"])
def get_allAttributes():
    database = get_db()
    query = """SELECT attribute_id,attribute_name, attribute_data_type, validation_data FROM attributes;"""
    with database.connection() as conn:
        res = conn.execute(query)
        allAttributes = res.fetchall()
        allAttributes_listed = extract_attributes(allAttributes)
        return json.dumps(allAttributes_listed)


@bp.route("/allTypes", methods=["GET"])
def get_allTypes():
    database = get_db()
    query_a = """SELECT type_id, type_name FROM types;"""
    with database.connection() as conn:
        res = conn.execute(query_a)
        allTypes = res.fetchall()
        allTypes_listed = []
        for type in allTypes:
            query_b = """SELECT at.attribute_id,attribute_name, attribute_data_type, validation_data FROM attributes_in_types AS at INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id INNER JOIN types AS t on at.type_id = t.type_id WHERE t.type_id = %(type_id)s;"""
            res = conn.execute(query_b, {"type_id": type[0]})
            attributes = extract_attributes(res.fetchall())
            allTypes_listed.append(
                {"typeId": type[0], "typeName": type[1],
                    "metadata": attributes}
            )
        return json.dumps(allTypes_listed), 200


@bp.route("/delete/<id>", methods=["POST"])
def delete_type(id):
    database = get_db()
    canDo = True

    query = """SELECT COUNT(*) FROM assets WHERE type = (%(id)s);"""
    with database.connection() as conn:
        res = conn.execute(query, {"id": id})
        if (res.fetchone()[0] > 0):
            canDo = False

    query = """SELECT COUNT(*) FROM type_link WHERE type_id_to = (%(id)s);"""
    with database.connection() as conn:
        res = conn.execute(query, {"id": id})
        if (res.fetchone()[0] > 0):
            canDo = False

    if canDo:
        query = """DELETE FROM type_link WHERE type_id_from = (%(id)s);"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

        query = """DELETE FROM attributes_in_types WHERE type_id = (%(id)s);"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

        query = """DELETE FROM types WHERE type_id = (%(id)s);"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

    return {"msg": "", "wasAllowed": canDo}, 200


@bp.route("/attribute/delete/<id>", methods=["POST"])
def delete_attribute(id):
    database = get_db()
    canDo = True

    query = """SELECT COUNT(*) FROM attributes_in_types WHERE attribute_id = (%(id)s)"""
    with database.connection() as conn:
        res = conn.execute(query, {"id": id})
        if (res.fetchone()[0] > 0):
            canDo = False

    if canDo:
        query = """DELETE FROM attributes WHERE attribute_id = (%(id)s)"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

    return {"msg": "", "wasAllowed": canDo}, 200
