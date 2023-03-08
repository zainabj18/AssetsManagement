from datetime import datetime, timedelta
import json

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
def getUsers():
    database = get_db()
    query = """SELECT * FROM accounts;"""
    with database.connection() as conn:
        result = conn.execute(query)
        usersfetched = result.fetchall()
    return json.dumps(usersfetched), 200

def insertUsers():
    database = get_db()
    query = """INSERT INTO accounts 
                VALUES (1,'John','Smith','John_Smith123','hello12345','VIEWER','PUBLIC');"""
    with database.connection() as conn:
        result = conn.execute(query)
