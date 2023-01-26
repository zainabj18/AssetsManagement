from functools import wraps

import jwt
from flask import current_app, request

from app.db import UserRole


def protected(role=UserRole.VIEWER):
    def decorated_route(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            if "x-access-token" in request.headers:
                token = request.headers["x-access-token"]
            else:
                return {
                    "msg": "Please provide a valid token in the header",
                    "error": "Missing Token",
                }, 401
            try:
                data = jwt.decode(
                    token,
                    current_app.config["SECRET_KEY"],
                    algorithms=[current_app.config["JWT_ALGO"]],
                )
            except jwt.ExpiredSignatureError as e:
                return {"msg": str(e), "error": "Invalid Token"}, 401
            if UserRole(data["account_type"]) < role:
                return {
                    "msg": "Your account is unauthorised to acces this please speak to your admin",
                    "error": "Invalid Token",
                }, 401

            return func(data["account_id"], data["account_privileges"], *args, **kwargs)

        return wrapper

    return decorated_route
