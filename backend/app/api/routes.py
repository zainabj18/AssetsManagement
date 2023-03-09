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


@bp.errorhandler(401)
def unathorised(e):
    return e.description, 401


bp.register_blueprint(auth_bp)
bp.register_blueprint(asset_bp)
bp.register_blueprint(type_bp)
bp.register_blueprint(tag_bp)
bp.register_blueprint(project_bp)
