from app.db import get_db
from flask import Blueprint


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/accountmanager", methods=["GET"])
def getUsers():
    database = get_db()
    query = """SELECT account_id,first_name,last_name,username FROM accounts;"""
    with database.connection() as conn:
        result = conn.execute(query)
        usersfetched = result.fetchall()
        usersfetched_listed = extract_people(usersfetched)
    return {"data":usersfetched_listed}, 200

def extract_people(people):
    allPeople_listed = []
    for person in people:
        allPeople_listed.append(
                { 
                    "accountID": person[0],
                    "firstName": person[1],
                    "lastName": person[2],
                    "username": person[3]
                }
        )
    return allPeople_listed

"""@bp.route("/accountmanager", methods=["GET"])
def fetchUsers(searched):
    database = get_db()
    query = ""SELECT username FROM accounts WHERE username LIKE %(searched)s 
            OR username LIKE %(wildcard)s;"",{"searched":f"%{searched}%","wildcard":f"_{searched}%"}
    with database.connection() as conn:
        result = conn.execute(query)
        searched_users = result.fetchall()
        searched_users_listed = extract_searched_users(searched_users)
    return {"data":searched_users_listed}, 200"""

"""def extract_searched_users(users):
    listed_users = []
    for user in users:
        listed_users.append(
            {
                "username": user[0]
            }
        )
    return listed_users"""
        