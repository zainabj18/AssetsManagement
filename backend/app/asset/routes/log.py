
from app.core.utils import protected
from app.db import UserRole, get_db
from flask import Blueprint
from .. import services
bp = Blueprint("logs", __name__, url_prefix="/logs")

@bp.route("/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def logs(id, user_id, access_level):
    db = get_db()
    services.abort_asset_not_exists(db=db,asset_id=id)
    return {"data":services.get_asset_logs(db,id)}
