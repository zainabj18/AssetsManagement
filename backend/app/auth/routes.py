from datetime import datetime, timedelta

import jwt
from app.core.utils import decode_token, protected
from app.db import UserRole, get_db
from app.schemas import UserCreate, UserInDB
from flask import Blueprint, current_app, jsonify, request
from psycopg import Error
from psycopg.rows import class_row
from pydantic.error_wrappers import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")

def create_user(db, user):
    with db.connection() as conn:
        conn.execute(
            """
        INSERT INTO accounts (first_name,last_name,username, hashed_password, account_type,account_privileges)
VALUES (%(first_name)s,%(last_name)s,%(username)s,%(password)s,%(acc_type)s,%(acc_priv)s);""",
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": generate_password_hash(user.password.get_secret_value()),
                "acc_type": user.account_type,
                "acc_priv": user.account_privileges,
            },
        )


def get_user(db, username):
    with db.connection() as conn:
        with conn.cursor(row_factory=class_row(UserInDB)) as cur:
            cur.execute(
                """SELECT * FROM accounts WHERE username=%(username)s;""",
                {"username": username},
            )
            user_in_db = cur.fetchone()
            return user_in_db


def get_user_by_id(db, user_id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT username FROM accounts WHERE account_id=%(user_id)s;""",
                {"user_id": user_id},
            )
            return cur.fetchone()

"""
    Creates a new user account in the database.

    Args:
    - db: Database object to execute the query against
    - user: User object to create the account with

    Returns: None
    """
    
@bp.route("/register", methods=["POST"])
def register():
    try:
        user = UserCreate(**request.json)
        db = get_db()
        if get_user(db, user.username) is not None:
            return (
                jsonify(
                    {
                        "msg": "User already exist with the same username please try a different one.",
                        "error": "Username already exist",
                    }
                ),
                400,
            )
    except ValidationError as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": e.errors(),
                    "error": "Failed to create user from on data provided",
                }
            ),
            400,
        )
    except Error as e:
        # TODO:Add an error enum
        return {"msg": str(e), "error": "Database Connection Error"}, 500

    try:
        create_user(db, user)
    except Error as e:
        # TODO:Add an error enum
        return {"msg": str(e), "error": "Database Connection Error"}, 500

    return {"msg": "User registered"}, 201

"""
Endpoint to handle user login.

POST request with a JSON payload containing the 'username' and 'password' fields.
Returns a JSON response with a message and data containing the user ID, username, user role, user privileges, and an access token cookie for the user.

If the username or password is not provided or is an empty string, returns a 400 Bad Request error.
If the user does not exist in the database, returns a 401 Unauthorized error.
If there is a database connection error, returns a 500 Internal Server Error.
If the provided password does not match the hashed password in the database, returns a 401 Unauthorized error.
"""
@bp.route("/login", methods=["POST"])
def login():
    request_dict = dict(request.json)
    username = request_dict.get("username", None)
    pwd = request_dict.get("password", None)
    if not username or not pwd or username == "" or username == "":
        return {
            "msg": "username and password required",
            "error": "Invalid credentials",
        }, 400

    db = get_db()
    try:
        if not (user_in_db := get_user(db, username)):
            return {"msg": "account doesn't exist", "error": "Invalid credentials"}, 401
    except Error as e:
        return {"msg": str(e), "error": "Database Connection Error"}, 500
    if not check_password_hash(user_in_db.hashed_password.get_secret_value(), pwd):
        return {
            "msg": "invalid username/password combination",
            "error": "Invalid credentials",
        }, 401

    token = jwt.encode(
        {
            "account_id": int(user_in_db.account_id),
            "account_type": user_in_db.account_type.value,
            "account_privileges": user_in_db.account_privileges.value,
            "exp": datetime.utcnow() + timedelta(minutes=160),
        },
        current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGO"],
    )
    resp = jsonify(
        {
            "msg": "logged in",
            "data": {
                "userID": int(user_in_db.account_id),
                "userRole": user_in_db.account_type.value,
                "username": username,
                "userPrivileges": user_in_db.account_privileges.value,
            },
        }
    )
    resp.set_cookie(
        "access-token",
        value=token,
        secure=True,
        httponly=True,
        expires=datetime.utcnow() + timedelta(hours=6),
    )
    return resp


@bp.route("/admin-status", methods=["GET"])
@protected(role=UserRole.ADMIN)
def is_admin(user_id, access_level):
    return {
        "msg": f"{user_id} You have admin privileges and data access level of {access_level.value}"
    }, 200


@bp.route("/user-status", methods=["GET"])
@protected(role=UserRole.USER)
def is_user(user_id, access_level):
    return {
        "msg": f"{user_id} You have user privileges and data access level of {access_level.value}"
    }, 200


@bp.route("/viewer-status", methods=["GET"])
@protected(role=UserRole.VIEWER)
def is_viewer(user_id, access_level):
    return {
        "msg": f"{user_id} You have viewer privileges and data access level of {access_level.value}"
    }, 200


@bp.route("/identify", methods=["GET"])
def identify():
    data = decode_token(request)
    db = get_db()
    try:
        if username := get_user_by_id(db, data["account_id"]):
            username = username[0]
    except Error as e:
        return {"msg": str(e), "error": "Database Connection Error"}, 500

    resp = jsonify(
        {
            "msg": "found you",
            "data": {
                "userID": data["account_id"],
                "userRole": data["account_type"],
                "username": username,
                "userPrivileges": data["account_privileges"],
            },
        }
    )
    return resp


@bp.route("/logout", methods=["DELETE"])
def logout():
    resp = jsonify({"msg": "logged out", "data": {}})
    resp.set_cookie("access-token", "", expires=0)
    return resp
