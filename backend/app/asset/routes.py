from flask import Blueprint, jsonify, request
from psycopg.rows import class_row
from pydantic import ValidationError

from app.core.utils import protected
from app.db import DataAccess, UserRole, get_db
from app.schemas import AssetBase, AssetBaseInDB

bp = Blueprint("asset", __name__, url_prefix="/asset")
import json


@bp.route("/", methods=["POST"])
def create():
    try:
        try:
            asset = AssetBase(**request.json)
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
    db_asset = asset.dict(exclude={"metadata"})
    db_asset["metadata"] = [json.dumps(x.dict()) for x in asset.metadata]
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO assets (name,link,type,description, classification)
    VALUES (%(name)s,%(link)s,%(type)s,%(description)s,%(classification)s)  RETURNING asset_id;""",
                db_asset,
            )
            asset_id=cur.fetchone()[0]
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

    return jsonify({"msg": "Added asset","data":asset_id}), 200


@bp.route("/classifications", methods=["GET"])
@protected(role=UserRole.USER)
def get_classifications(user_id, access_level):
    viwable_classifications = []
    for c in DataAccess:
        if c <= access_level:
            viwable_classifications.append(c.value)

    return {"data": viwable_classifications}


@bp.route("/<id>", methods=["GET"])
def view(id):
    db = get_db()
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute("""SELECT * FROM assets WHERE asset_id=%(id)s;""", {"id": id})
            asset = cur.fetchone()
    return asset.json(), 200
