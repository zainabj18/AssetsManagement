from functools import wraps

import jwt
import json
from app.db import DataAccess, UserRole
from flask import abort, current_app, request,jsonify
from pydantic import ValidationError
from psycopg import Error
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row
from enum import Enum,auto
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
                abort(403)
            return func(
                user_id=data["account_id"],
                access_level=DataAccess(data["account_privileges"]),
                **kwargs
            )

        return wrapper

    return decorated_route


class QueryResult(Enum):
    ONE = auto()
    ALL =auto()
    ALL_JSON =auto()

def audit_log_event(db,model_id,account_id,object_id,diff_dict,action):
    return run_query(db,"""
                INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
        VALUES (%(model_id)s,%(account_id)s,%(object_id)s,%(diff)s,%(action)s);""",
        {"model_id":model_id,"account_id":account_id,"object_id":object_id,"diff":json.dumps(diff_dict),"action":action})

def run_query(db, query, params=None,row_factory=dict_row,return_type=None):
    try:
        with db.connection() as db_conn:
            with db_conn.cursor(row_factory=row_factory) as cur:    
                if params == None:
                    cur.execute(query)
                else:
                    cur.execute(query, params)
                
                db_conn.commit()


                match return_type:
                    case QueryResult.ONE:
                        i=cur.fetchone()
                        return i
                    case QueryResult.ALL:
                        return cur.fetchall()
                    case QueryResult.ALL_JSON:
                        return [json.loads(row.json(by_alias=True)) for row in cur.fetchall()]
                    case _:
                        return       
    except Error as e:
        abort(500,{"msg": "Database Error","data":[str(e)]})

def model_creator(model,err_msg,*args, **kwargs):
    try:
        try:
            obj = model(*args, **kwargs)
        except ValidationError as e:
            abort(400,{"msg": err_msg,
                    "data": e.errors()
                })
    except:
        abort(400,{"msg": "Data provided is invalid",
                    "data": ["Invalid data"]
                })

    return obj