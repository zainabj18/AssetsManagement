from flask import Blueprint

from app.asset.routes import bp as asset_bp
from app.auth.routes import bp as auth_bp
from app.core.config import settings
from app.project.routes import bp as project_bp
from app.tag.routes import bp as tag_bp
from app.type.routes import bp as type_bp

bp = Blueprint("api", __name__, url_prefix=settings.APPLICATION_ROOT_URL)


@bp.route("/")
def index():
    return {
        "msg": "Hello World!",
        "version": settings.API_VERSION,
        "url": settings.APPLICATION_ROOT_URL,
    }


@bp.errorhandler(401)
def unathorised(e):
    return e.description, 401


bp.register_blueprint(auth_bp)
bp.register_blueprint(asset_bp)
bp.register_blueprint(type_bp)
bp.register_blueprint(tag_bp)
bp.register_blueprint(project_bp)
