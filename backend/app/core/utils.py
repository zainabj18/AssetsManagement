from functools import wraps

import jwt
from flask import current_app, request,abort

from app.db import UserRole,DataAccess
def decode_token(request):
    token = request.cookies.get('access-token')
    if not token:
        abort(401,{
            "msg": "Please provide a valid token in the header",
            "error": "Missing Token",
        })
    try:
        data = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=[current_app.config["JWT_ALGO"]],
        )
        return data
    except jwt.ExpiredSignatureError as e:
        abort(401,{"msg": str(e), "error": "Invalid Token"})



def protected(role=UserRole.VIEWER):
    def decorated_route(func):
        @wraps(func)
        def wrapper():
            data=decode_token(request)
            if UserRole(data["account_type"]) < role:
                return {
                    "msg": "Your account is forbidden to access this please speak to your admin",
                    "error": "Invalid Token",
                }, 403
            return func(data["account_id"],DataAccess(data["account_privileges"]))

        return wrapper

    return decorated_route
