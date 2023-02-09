from datetime import datetime, timedelta

import jwt
from app.core.utils import protected
from app.db import UserRole, get_db
from app.schemas import UserCreate, UserInDB
from flask import Blueprint, current_app, jsonify, request
from psycopg import Error
from psycopg.rows import class_row
from pydantic.error_wrappers import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/accountmanager", methods=["GET"])
def types():
    return {"msg": ""}, 200
