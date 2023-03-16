from app.db import get_db
from flask import Blueprint

bp = Blueprint("graphs", __name__, url_prefix="/graph")

@bp.route("/assets", methods=["GET"])
def get_assets():
    return {}, 200