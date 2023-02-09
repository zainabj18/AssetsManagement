from flask import Blueprint, jsonify, request
from psycopg.rows import class_row,dict_row
from pydantic import ValidationError

from app.core.utils import protected
from app.db import DataAccess, UserRole, get_db
from app.schemas import Asset, AssetBaseInDB,AttributeInDB,AssetOut

bp = Blueprint("asset", __name__, url_prefix="/asset")
import json


@bp.route("/", methods=["POST"])
def create():
    print(request.json)
    try:
        try:
            asset = Asset(**request.json)
        except ValidationError as e:
            return (
                jsonify(
                    {
                        "msg": "Data provided is invalid",
                        "data": e.errors(),
                        "error": "Failed to create asset from the data provided",
                    }
                ),
                400,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": None,
                    "error": "Failed to create asset from the data provided",
                }
            ),
            400,
        )
    db = get_db()
    print(asset)
    db_asset = asset.dict(exclude={"metadata"})

    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO assets (name,link,type,description, classification)
    VALUES (%(name)s,%(link)s,%(type)s,%(description)s,%(classification)s)  RETURNING asset_id;""",
                db_asset,
            )
            asset_id=cur.fetchone()[0]
            print(asset_id)
            for tag in asset.tags:
                cur.execute(
                    """
                INSERT INTO assets_in_tags (asset_id,tag_id)
        VALUES (%(asset_id)s,%(tag_id)s);""",
                    {"asset_id":asset_id,"tag_id":tag},
                )
            for project in asset.projects:
                cur.execute(
                    """
                INSERT INTO assets_in_projects (asset_id,project_id)
        VALUES (%(asset_id)s,%(project_id)s);""",
                    {"asset_id":asset_id,"project_id":project},
                )
            for attribute in asset.metadata:
                cur.execute(
                    """
                INSERT INTO attributes_values (asset_id,attribute_id,value)
        VALUES (%(asset_id)s,%(attribute_id)s,%(value)s);""",
                    {"asset_id":asset_id,"attribute_id":attribute.attribute_id,"value":attribute.attribute_value},
                )

    return jsonify({"msg": "Added asset","data":asset_id}), 200


@bp.route("/classifications", methods=["GET"])
@protected(role=UserRole.USER)
def get_classifications(user_id, access_level):
    viwable_classifications = []
    for c in DataAccess:
        if c <= access_level:
            viwable_classifications.append(c.value)

    return {"data": viwable_classifications}

@bp.route("projects/<id>", methods=["GET"])
def list_asset_project(id):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""SELECT projects.* FROM assets_in_projects
    INNER JOIN projects on projects.id=assets_in_projects.project_id WHERE asset_id=%(id)s;""", {"id": id})
                selected_projects=(list(cur.fetchall()))
                for x in selected_projects:
                    x["isSelected"]=True
                cur.execute("""SELECT * FROM projects WHERE id not in (SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s);""", {"id": id})
                projects=(list(cur.fetchall()))
                
                #SELECT * FROM projects WHERE id not in (1);
    return {"data": selected_projects+projects}, 200

@bp.route("/<id>", methods=["GET"])
def view(id):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute("""SELECT * FROM assets WHERE asset_id=%(id)s AND soft_delete=0;""", {"id": id})
            asset = cur.fetchone()
            print(asset)
        with db_conn.cursor(row_factory=class_row(AttributeInDB)) as cur:
            cur.execute("""SELECT attributes.attribute_id,attribute_name, attribute_data_type as attribute_type, validation_data,value as attribute_value FROM attributes_values 
INNER JOIN attributes on attributes.attribute_id=attributes_values.attribute_id WHERE asset_id=%(id)s;""", {"id": id})
            metadata=(cur.fetchall())
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT projects.* FROM assets_in_projects
INNER JOIN projects on projects.id=assets_in_projects.project_id WHERE asset_id=%(id)s;""", {"id": id})
            projects=(list(cur.fetchall()))
            cur.execute("""SELECT tags.id,name FROM assets_in_tags 
INNER JOIN tags on tags.id=assets_in_tags.tag_id WHERE asset_id=%(id)s;""", {"id": id})
            tags=(list(cur.fetchall()))
            print(tags)
            print(asset)
            cur.execute("""SELECT type_name FROM types WHERE type_id=%(id)s;""", {"id": asset.type})
            type=cur.fetchone()["type_name"]

        asset=AssetOut(**asset.dict(),metadata=metadata,projects=projects,tags=tags)
        asset.type=type
        print(asset)
    return {"data": json.loads(asset.json(by_alias=True))}, 200

@bp.route("/<id>", methods=["DELETE"])
def delete(id):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute("""UPDATE assets SET soft_delete = %(del)s WHERE asset_id=%(id)s;""", {"id": id,"del":1})

    return {}, 200