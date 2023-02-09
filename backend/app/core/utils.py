from functools import wraps

import jwt
from flask import abort, current_app, request

from app.db import DataAccess, UserRole


def decode_token(request):
    token = request.cookies.get("access-token")
    if not token:
        abort(
            401,
            {
                "msg": "Please provide a valid token in the header",
                "error": "Missing Token",
            },
        )
    try:
        data = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGO"]],
        )
        return data
    except jwt.ExpiredSignatureError as e:
        abort(401, {"msg": str(e), "error": "Invalid Token"})
    except jwt.InvalidSignatureError as e:
        abort(401, {"msg": str(e), "error": "Invalid Token"})


def protected(role=UserRole.VIEWER):
    def decorated_route(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = decode_token(request)
            if UserRole(data["account_type"]) < role:
                return {
                    "msg": "Your account is forbidden to access this please speak to your admin",
                    "error": "Invalid Token",
                }, 403
            return func(user_id=data["account_id"],access_level=DataAccess(data["account_privileges"]),**kwargs)

        return wrapper

    return decorated_route
