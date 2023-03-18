
from flasgger import swag_from
from flask import Blueprint,request
from http import HTTPStatus
from app.core.utils import protected,model_creator,audit_log_event
from app.db import UserRole, get_db,Actions,Models,DataAccess
from app.schemas import Comment,CommentOut
from .services import fetch_assets_by_tag_count
bp = Blueprint("related", __name__, url_prefix="/related")

@bp.route("/tags/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def related_tags(id,user_id, access_level):
    db = get_db()
    return {"data": fetch_assets_by_tag_count(db,id,access_level)}



# @bp.route("/projects/<id>", methods=["GET"])
# @protected(role=UserRole.VIEWER)
# def related_projects(id,user_id, access_level):
#     #get all the assets that belong to the same project as an asset
#     db = get_db()
#     assets_json = []
#     with db.connection() as db_conn:
#         with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
#             cur.execute(
#                 """
#                 WITH related_asset_projects as (SELECT COUNT(asset_id),asset_id FROM assets_in_projects WHERE project_id in (SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s) and asset_id !=%(id)s
# GROUP BY asset_id
# HAVING COUNT(asset_id)>0)
# SELECT assets.*,related_asset_projects.count FROM assets
# INNER JOIN related_asset_projects on assets.asset_id=related_asset_projects.asset_id
# ORDER BY count DESC;""",
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
