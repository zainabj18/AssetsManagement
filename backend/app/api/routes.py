from flask import Blueprint

from app.asset.routes import bp as asset_bp
from app.auth.routes import bp as auth_bp
from app.core.config import settings
from app.type.routes import bp as type_bp
from app.projects.routes import bp as project_bp

bp = Blueprint("api", __name__, url_prefix=settings.APPLICATION_ROOT_URL)


@bp.route("/")
def index():
    return {
        "msg": "Hello World!",
        "version": settings.API_VERSION,
        "url": settings.APPLICATION_ROOT_URL,
    }


bp.register_blueprint(auth_bp)
bp.register_blueprint(asset_bp)
bp.register_blueprint(type_bp)
bp.register_blueprint(project_bp)
