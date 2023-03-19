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
from app.core.utils import protected,run_query,model_creator,QueryResult
from app.schemas import Log
from psycopg.rows import class_row
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


@bp.errorhandler(401)
def unathorised(e):
    return e.description, 401

@bp.errorhandler(400)
def invalid_request(e):
    return e.description, 400

bp.register_blueprint(auth_bp)
bp.register_blueprint(asset_bp)
bp.register_blueprint(type_bp)
bp.register_blueprint(tag_bp)
bp.register_blueprint(project_bp)
