from app.asset.routes import bp as asset_bp
from app.auth.routes import bp as auth_bp
from app.core.config import settings
from app.project.routes import bp as project_bp
from app.tag.routes import bp as tag_bp
from app.type.routes import bp as type_bp
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

from psycopg.rows import dict_row
from app.auth.routes import get_user_by_id

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
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT model_name,object_id,date,account_id,action FROM public.audit_logs
INNER JOIN tracked_models ON tracked_models.model_id=audit_logs.model_id
ORDER BY date ASC;""",
                {"asset_id": id},
            )
            logs = cur.fetchall()
            print(logs)
            for log in logs:
                if username := get_user_by_id(db,log["account_id"]):
                    username = username[0]
                log["username"]=username
    return {"data":logs}

"""
Handle HTTP 401 Unauthorized errors.

Args:
    e (HTTPException): The HTTP 401 Unauthorized error that was raised.

Returns:
    A tuple containing the error message and the HTTP status code to be returned to the client:
    - The error message is obtained from the 'description' attribute of the HTTPException object.
    - The HTTP status code is set to 401.
"""

@bp.errorhandler(401)
def unathorised(e):
    return e.description, 401


bp.register_blueprint(auth_bp)
bp.register_blueprint(asset_bp)
bp.register_blueprint(type_bp)
bp.register_blueprint(tag_bp)
bp.register_blueprint(project_bp)
