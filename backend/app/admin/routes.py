import json
from app.db import get_db
from flask import Blueprint
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
    database = get_db()
    query = """DELETE FROM accounts;"""
    with database.connection() as conn:
        conn.execute(query)
    return {"message":"Users deleted successfully"}, 200