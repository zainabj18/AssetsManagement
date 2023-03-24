import json

from app.db import get_db
from app.schemas import AttributeBase, Type
from flask import Blueprint, request
from psycopg.rows import dict_row


def make_query(db, query, params=None):
    with db.connection() as conn:
        if params == None:
            return conn.execute(query)
        return conn.execute(query, params)


def get_types(db):
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM types;""")
            return cur.fetchall()


bp = Blueprint("type", __name__, url_prefix="/type")

"""Create a new Type in the database.

    Extracts the Type object from the request JSON and uses it to create a new Type in the database. The Type object should
    contain a "metadata" field with a list of Attribute objects and a "depends_on" field with a list of type IDs that this Type
    depends on. 

    Returns:
        A dictionary with a "msg" key that indicates whether the operation was successful, and a status code.

    Raises:
        N/A
"""

@bp.route("/new", methods=["POST"])
def add_type():
    new_type = Type(**request.json)
    db_type = new_type.dict(exclude={"metadata", "depends_on"})
    database = get_db()

    query = """
    SELECT MAX(version_number) FROM type_version
    INNER JOIN types ON types.type_id = type_version.type_id
    WHERE type_name = %(type_name)s;
    """
    result = make_query(database, query, db_type)
    type_version_number = 1
    res_id = result.fetchone()[0]
    if res_id is not None:
        type_version_number = res_id + 1

    if type_version_number == 1:
        query = """INSERT INTO types (type_name) VALUES (%(type_name)s) RETURNING type_id;"""
    else:
        query = """SELECT type_id FROM types WHERE type_name = %(type_name)s"""

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

"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""

@bp.route("/version/names", methods=["GET"])
def list_type_names_with_versions():
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""WITH ranked_types AS (
SELECT *,
       rank() OVER (PARTITION BY type_id ORDER BY version_number DESC) as row_rank
FROM type_version)

SELECT version_id,type_name FROM ranked_types 
INNER JOIN types ON types.type_id=ranked_types.type_id
WHERE row_rank=1""")
            types=cur.fetchall()

    return {"msg": "types-w-versions", "data": types}, 200
"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""

@bp.route("/adder/new", methods=["POST"])
def add_attribute():
    new_attribute = AttributeBase(**request.json)
    db_attribute = new_attribute.dict(exclude={"validation_data"})
    db_attribute["validation_data"] = json.dumps(new_attribute.validation_data)
    database = get_db()
    query = """INSERT INTO attributes (attribute_name, attribute_data_type, validation_data) VALUES (%(attribute_name)s, %(attribute_data_type)s, %(validation_data)s);"""
    with database.connection() as conn:
        conn.execute(query, db_attribute)
    return {"msg": ""}, 200

"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""


@bp.route("/<id>", methods=["GET"])
def get_type(id):
    database = get_db()
    query = """
    SELECT t.type_id, type_name, version_id, version_number
    FROM types as t
    INNER JOIN type_version as tv ON t.type_id = tv.type_id
    WHERE tv.version_id = %(id)s;
    """
    res = make_query(database, query, {"id": id})
    type = res.fetchone()

    query = """
    SELECT at.attribute_id,attribute_name, attribute_data_type, validation_data
    FROM attributes_in_types AS at
    INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id
    INNER JOIN type_version AS tv on at.type_version = tv.version_id
    WHERE tv.version_id = %(id)s;
    """
    res = make_query(database, query, {"id": id})
    attributes = extract_attributes(res.fetchall())

    query = """SELECT version_id,type_name FROM type_names_versions
WHERE version_id IN (SELECT type_version_to FROM type_version_link WHERE type_version_from=%(id)s);"""
    res = make_query(database, query, {"id": id})
    rows=res.fetchall()
    depends_on = [value[0] for value in rows]
    depends_on_names = [value[1] for value in rows]
    return {
        "typeId": type[0],
        "typeName": type[1],
        "versionId": type[2],
        "versionNumber": type[3],
        "metadata": attributes,
        "dependsOn": depends_on,
        "dependsOnNames": depends_on_names
    }, 200


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
        return {"data":allAttributes_listed}

"""_summary_
api:GET
description: get all the types 
    Returns:
   
        json data
"""
@bp.route("/allTypes", methods=["GET"])
def get_allTypes():
    database = get_db()
    query = """
    SELECT version_id, t.type_id, t.type_name, version_number
    FROM types as t
    INNER JOIN type_version as tv ON t.type_id = tv.type_id
    ORDER BY t.type_name, version_number;
    """
    res = make_query(database, query)
    allTypes = res.fetchall()
    allTypes_listed = []
    for type in allTypes:
        query = """
        SELECT at.attribute_id, attribute_name, attribute_data_type, validation_data
        FROM attributes_in_types AS at
        INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id
        INNER JOIN type_version AS tv on at.type_version = tv.version_id
        WHERE version_id = %(version_id)s;
        """
        res = make_query(database, query, {"version_id": type[0]})
        attributes = extract_attributes(res.fetchall())
        allTypes_listed.append(
            {
                "versionId": type[0],
                "typeId": type[1],
                "typeName": type[2],
                "versionNumber": type[3],
                "metadata": attributes
            }
        )
    return {"data":allTypes_listed}

"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""

@bp.route("/delete/<id>", methods=["POST"])
def delete_type(id):
    database = get_db()
    canDo = True

    query = """SELECT version_id FROM type_version WHERE type_id = %(id)s"""
    res = make_query(database, query, {"id": id})
    version_ids = res.fetchall()

    for version_id in version_ids:
        query = """SELECT COUNT(*) FROM assets WHERE version_id = (%(id)s);"""
        res = make_query(database, query, {"id": version_id[0]})
        if (res.fetchone()[0] > 0):
            canDo = False
            break

        query = """SELECT COUNT(*) FROM type_version_link WHERE type_version_to = (%(id)s);"""
        res = make_query(database, query, {"id": version_id[0]})
        if (res.fetchone()[0] > 0):
            canDo = False
            break

    if canDo:
        query = """
        DELETE FROM type_version_link
        USING type_version
        WHERE version_id = type_version_from
            AND type_id = %(id)s;
        """
        make_query(database, query, {"id": id})

        query = """
        DELETE FROM attributes_in_types
        USING type_version
        WHERE version_id = type_version
            AND type_id = %(id)s;
        """
        make_query(database, query, {"id": id})

        query = """DELETE FROM type_version WHERE type_id = %(id)s;"""
        make_query(database, query, {"id": id})

        query = """DELETE FROM types WHERE type_id = %(id)s;"""
        make_query(database, query, {"id": id})

    return {"msg": "", "wasAllowed": canDo}, 200

"""_summary_
 Parameters:
    id : The ID all the assets that belong to the same project .
    Returns:
        json data
"""
@bp.route("/attribute/delete/<id>", methods=["POST"])
def delete_attribute(id):
    database = get_db()
    canDo = True

    query = """SELECT COUNT(*) FROM attributes_in_types WHERE attribute_id = (%(id)s)"""
    with database.connection() as conn:
        res = conn.execute(query, {"id": id})
        if res.fetchone()[0] > 0:
            canDo = False

    if canDo:
        query = """DELETE FROM attributes WHERE attribute_id = (%(id)s)"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

    return {"msg": "", "wasAllowed": canDo}, 200


@bp.route("/adder/isAttrNameIn", methods=["POST"])
def is_attr_name_in():
    database = get_db()
    query = """SELECT COUNT(*) FROM attributes WHERE attribute_name = %(name)s"""
    res = make_query(database, query, {"name": request.json["name"]})
    is_in = res.fetchone()[0] > 0
    return {"data": is_in}, 200

"""
List the names of all the available types with their latest version number.

Returns:
    A JSON response with the list of names and their latest version number.
"""

@bp.route("/backfill", methods=["POST"])
def backfill():
    jason = request.json
    print(jason)
    database = get_db()
    key = {"id": request.json["version_id"]}
    print(key)
    query = """
    SELECT asset_id FROM assets
    WHERE version_id = %(id)s;
    """
    asset_ids = make_query(database, query, key).fetchall()

    query = """
    SELECT MAX(version_id)
    FROM type_version
    WHERE type_id = (
        SELECT type_id
        FROM type_version
        WHERE version_id = %(id)s 
    );
    """
    latest_version = make_query(database, query, key).fetchone()[0]

    if (latest_version == jason["version_id"]):
        return {"msg": "Given version is already the latest version."}, 400

    query_a = """
    UPDATE assets
    SET version_id = %(new_id)s
    WHERE asset_id = %(asset_id)s;
    """
    query_b = """
    INSERT INTO attributes_values (attribute_id, asset_id, attribute_value)
    VALUES (%(attribute_id)s, %(asset_id)s, %(value)s)
    """

    for asset_id in asset_ids:
        key_a = {
            "new_id": latest_version,
            "asset_id": asset_id[0]
        }
        for attribute in jason["attributes"]:
            key_b = {
                "attribute_id": attribute["attributeID"],
                "asset_id": asset_id[0],
                "value": attribute["data"]
            }
            make_query(database, query_b, key_b)
        make_query(database, query_a, key_a)
    return {"msg": ""}, 200
