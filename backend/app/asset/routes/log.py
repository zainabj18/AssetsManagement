from flask import Blueprint

from app.core.utils import protected
from app.db import UserRole, get_db

from ..services import get_asset_logs
from ..utils import can_view_asset

bp = Blueprint("logs", __name__, url_prefix="/logs")


@bp.route("/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def logs(id, user_id, access_level):
    db = get_db()
    can_view_asset(db=db, asset_id=id, access_level=access_level)
    return {"data": get_asset_logs(db, id)}
