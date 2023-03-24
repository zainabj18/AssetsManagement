from app.asset.routes import bp as asset_bp
from app.auth.routes import bp as auth_bp
from app.core.config import settings
from app.project.routes import bp as project_bp
from app.tag.routes import bp as tag_bp
from app.type.routes import bp as type_bp
from app.admin.routes import bp as admin_bp
from app.graphs.routes import bp as graph_bp
from flask import Blueprint
bp = Blueprint("api", __name__, url_prefix=settings.APPLICATION_ROOT_URL)


@bp.route("/")
def index():
    return {
        "msg": "Hello World!",
        "version": settings.API_VERSION,
        "url": settings.APPLICATION_ROOT_URL,
    }

from app.core.utils import protected
from app.db import UserRole, get_db 
from app.core.utils import protected,run_query,model_creator,QueryResult
from app.schemas import Log
from psycopg.rows import class_row

"""
Retrieve audit logs from the database for a given user and access level.

Args:
    user_id (int): The ID of the user for which to retrieve audit logs.
    access_level (str): The access level of the user for which to retrieve audit logs.

Returns:
    A dictionary containing a list of audit logs for the specified user and access level:
    - 'data': a list of dictionaries, where each dictionary represents a single audit log and has the following keys:
        - 'model_name': the name of the tracked model associated with the audit log
        - 'object_id': the ID of the object associated with the audit log
        - 'date': the date and time the audit log was generated
        - 'account_id': the ID of the user associated with the audit log
        - 'action': the action that was performed on the tracked model
        - 'username': the username of the user associated with the audit log
"""
@bp.route("/logs", methods=["GET"])
@protected(role=UserRole.VIEWER)
def logs(user_id, access_level):
    db = get_db()
    logs=run_query(db,"""
    SELECT model_name,audit_logs.*,accounts.username FROM audit_logs
INNER JOIN tracked_models ON tracked_models.model_id=audit_logs.model_id
INNER JOIN accounts ON audit_logs.account_id=accounts.account_id
ORDER BY date ASC;""",return_type=QueryResult.ALL_JSON,row_factory=class_row(Log))
    return {"data":logs}

"""
Handle HTTP errors.

Args:
    e (HTTPException): The HTTP error that was raised via abort.

Returns:
    A tuple containing the error message and the HTTP status code to be returned to the client:
    - The error message is obtained from the 'description' attribute of the HTTPException object.
    - The HTTP status code is set to the respective http codes.
"""

@bp.errorhandler(401)
def unathorised(e):
    return e.description, 401

@bp.errorhandler(403)
def unathorised(e):
    return {
                    "msg": "Your account is forbidden to access this please speak to your admin",
                }, 403

@bp.errorhandler(400)
def invalid_request(e):
    return e.description, 400

@bp.errorhandler(422)
def unporcessible(e):
    return e.description, 422

@bp.errorhandler(404)
def resouce_not_found(e):
    return e.description, 404
@bp.errorhandler(500)
def interal_server_error(e):
    return e.description, 500

# add sub blueprints to the main api blueprint
bp.register_blueprint(auth_bp)
bp.register_blueprint(asset_bp)
bp.register_blueprint(type_bp)
bp.register_blueprint(tag_bp)
bp.register_blueprint(project_bp)
bp.register_blueprint(admin_bp)
bp.register_blueprint(graph_bp)
