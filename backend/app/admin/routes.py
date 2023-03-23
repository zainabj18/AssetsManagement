import json
from app.db import get_db
from flask import Blueprint, request
from enum import Enum


bp = Blueprint("admin", __name__, url_prefix="/admin")


def enum_converter(o):
    if isinstance(o, Enum):
        return o.name
    return o

@bp.route("/accountmanager", methods=["GET"])
def getUsers():
    database = get_db()
    query = """SELECT * FROM accounts;"""
    with database.connection() as conn:
        result = conn.execute(query)
        usersfetched = result.fetchall()
        usersfetched_listed = extract_people(usersfetched)
        usersfetched_listed = json.loads(json.dumps(usersfetched_listed, default=enum_converter))
    return {"data":usersfetched_listed}, 200

def extract_people(people):
    allPeople_listed = []
    for person in people:
        allPeople_listed.append(
                { 
                    "accountID": person[0],
                    "firstName": person[1],
                    "lastName": person[2],
                    "username": person[3],
                    "hashed_password": person[4],
                    "userRole": person[5],
                    "userPrivileges": person[6]
                }
        )
    return allPeople_listed
@bp.route("/accountmanager", methods=["DELETE"])
def deleteUsers():
    id = request.args.get('id')
    if (id == '1'):
        return {"msg": "Can not delete admin account"}, 401
    database = get_db()
    query = """DELETE FROM accounts WHERE account_id = %(id)s;"""
    with database.connection() as conn:
        conn.execute(query, {"id":id})
    return {"msg":"Users deleted successfully"}, 200