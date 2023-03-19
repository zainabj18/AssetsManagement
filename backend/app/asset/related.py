
from flasgger import swag_from
from flask import Blueprint,request
from http import HTTPStatus
from app.core.utils import protected,model_creator,audit_log_event
from app.db import UserRole, get_db,Actions,Models,DataAccess
from app.schemas import Comment,CommentOut
from .services import fetch_assets_by_common_count_count
bp = Blueprint("related", __name__, url_prefix="/related")

@bp.route("/tags/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_by_tags(id:int,user_id:int, access_level:DataAccess):
    """Finds assets that share the same tags.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A msg saying comment added.
    """
    db = get_db()
    return {"data": fetch_assets_by_common_count_count(db=db,asset_id=id,access_level=access_level,related_table="assets_in_tags",related_table_id="tag_id")}


@bp.route("/projects/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_by_projects(id:int,user_id:int, access_level:DataAccess):
    """Finds assets that share the same projects.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A msg saying comment added.
    """
    db = get_db()
    return {"data": fetch_assets_by_common_count_count(db=db,asset_id=id,access_level=access_level,related_table="assets_in_projects",related_table_id="project_id")}

@bp.route("/classification/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_by_projects(id:int,user_id:int, access_level:DataAccess):
    """Finds assets that share the same classification.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A msg saying comment added.
    """
    db = get_db()
    return {"data": fetch_assets_by_common_count_count(db=db,asset_id=id,access_level=access_level,related_table="assets_in_projects",related_table_id="project_id")}

# @bp.route("/classification/<id>", methods=["GET"])
# @protected(role=UserRole.VIEWER)
# def related_classification(id,user_id, access_level):
#     #get all the assets that belong to the same project as an asset
#     db = get_db()
#     assets_json = []
#     with db.connection() as db_conn:
#         with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
#             cur.execute(
#                 """
#                 SELECT * FROM assets WHERE classification=(SELECT classification FROM assets WHERE asset_id=%(id)s) AND asset_id!=%(id)s ORDER BY asset_id;""",
#                 {"id": id},
#             )
#             selected_assets = list(cur.fetchall())
 
#             assets = list(cur.fetchall())
#             selected_assets.extend(assets)
#         # gets the type name for each assset
#         with db_conn.cursor(row_factory=dict_row) as cur:
#             for a in selected_assets:
#                 if a.classification <= access_level:
#                     cur.execute(
#                         """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
# INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
#                         {"version_id": a.version_id},
#                     )
#                     type = cur.fetchone()["type_name"]
#                     aj = json.loads(a.json(by_alias=True))
#                     aj["type"] = type
#                     assets_json.append(aj)
#             res = jsonify({"data": assets_json})
#     return res


# @bp.route("/type/<id>", methods=["GET"])
# @protected(role=UserRole.VIEWER)
# def related_type(id,user_id, access_level):
#     #get all the assets that belong to the same project as an asset
#     db = get_db()
#     assets_json = []
#     with db.connection() as db_conn:
#         with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
#             cur.execute(
#                 """
#                 SELECT * FROM assets WHERE type=(SELECT type FROM assets WHERE asset_id=%(id)s) AND asset_id!=%(id)s ORDER BY asset_id;""",
#                 {"id": id},
#             )
#             selected_assets = list(cur.fetchall())
 
#             assets = list(cur.fetchall())
#             selected_assets.extend(assets)
#         # gets the type name for each assset
#         with db_conn.cursor(row_factory=dict_row) as cur:
#             for a in selected_assets:
#                 if a.classification <= access_level:
#                     cur.execute(
#                         """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
# INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
#                         {"version_id": a.version_id},
#                     )
#                     type = cur.fetchone()["type_name"]
#                     aj = json.loads(a.json(by_alias=True))
#                     aj["type"] = type
#                     assets_json.append(aj)
#             res = jsonify({"data": assets_json})
#     return res


# @bp.route("/from/<id>", methods=["GET"])
# @protected(role=UserRole.VIEWER)
# def related_from(id,user_id, access_level):
#     #get all the assets that belong to the same project as an asset
#     db = get_db()
#     assets_json = []
#     with db.connection() as db_conn:
#         with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
#             cur.execute(
# """SELECT assets.* FROM assets_in_assets
#     INNER JOIN assets on assets.asset_id=assets_in_assets.to_asset_id WHERE from_asset_id=%(id)s ORDER BY assets_in_assets.to_asset_id;""",
#                 {"id": id},
#             )
#             selected_assets = list(cur.fetchall())
 
#             assets = list(cur.fetchall())
#             selected_assets.extend(assets)
#         # gets the type name for each assset
#         with db_conn.cursor(row_factory=dict_row) as cur:
#             for a in selected_assets:
#                 if a.classification <= access_level:
#                     cur.execute(
#                         """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
# INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
#                         {"version_id": a.version_id},
#                     )
#                     type = cur.fetchone()["type_name"]
#                     aj = json.loads(a.json(by_alias=True))
#                     aj["type"] = type
#                     assets_json.append(aj)
#             res = jsonify({"data": assets_json})
#     return res


# @bp.route("/to/<id>", methods=["GET"])
# @protected(role=UserRole.VIEWER)
# def related_to(id,user_id, access_level):
#     #get all the assets that belong to the same project as an asset
#     db = get_db()
#     assets_json = []
#     with db.connection() as db_conn:
#         with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
#             cur.execute(
# """SELECT assets.* FROM assets_in_assets
# INNER JOIN assets on assets.asset_id=assets_in_assets.from_asset_id WHERE to_asset_id=%(id)s ORDER BY assets_in_assets.to_asset_id;""",
#                 {"id": id},
#             )
#             selected_assets = list(cur.fetchall())
 
#             assets = list(cur.fetchall())
#             selected_assets.extend(assets)
#         # gets the type name for each assset
#         with db_conn.cursor(row_factory=dict_row) as cur:
#             for a in selected_assets:
#                 if a.classification <= access_level:
#                     cur.execute(
#                         """SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
# INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",
#                         {"version_id": a.version_id},
#                     )
#                     type = cur.fetchone()["type_name"]
#                     aj = json.loads(a.json(by_alias=True))
#                     aj["type"] = type
#                     assets_json.append(aj)
#             res = jsonify({"data": assets_json})
#     return res
