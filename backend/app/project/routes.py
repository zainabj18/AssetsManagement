import json
from app.db import get_db
from app.schemas import Project
from flask import Blueprint, jsonify, request
from psycopg import Error
from psycopg.rows import dict_row
from pydantic import ValidationError

from backend.app.core.utils import decode_token

bp = Blueprint("project", __name__, url_prefix="/project")


def get_projects(db):
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM projects;""")
            pList = """SELECT project_id, name, description FROM PROJECTS"""
            allProjects = []
            for project in pList:
                query = """SELECT username, account_id
                FROM people_in_projects
                INNER JOIN accounts ON accounts.account_id = people_in_projects.account_id
                WHERE project_id = %(project_id)s;"""
                key = {"project_id":project.project_id}
                res = db_conn.execute(query, key)
                people = res.fetchall()
                accounts = []
                for account in people:
                    accounts.append({"accountName": account[0], "account_id": account[1]})
                allProjects.append({
                    "projectID": project[0],
                    "projectname":project[1],
                    "projectDescription":project[2],
                    "accounts":{
                        accounts
                    }
                })
    return {"data": allProjects}

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

def add_people_to_project(db,id,account_id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO people_in_projects(project_id,account_id)
            VALUES(%(project_id)s,%(account_id)s);
            """,{"account_id":account_id,"project_id":id})

def list_people(db):
    with db.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT account_id FROM people_in_projects;""")
            return cur.fetchall()

# def get_people(db):
#     with db.connection() as db_conn:
#         with db_conn.cursor(row_factory=dict_row) as cur:
#             cur.execute("""SELECT * FROM people_in_projects;""")
#             return cur.fetchall()
        
# def get_user_by_project(db):
#     with db.connection() as db_conn:
#         with db_conn.cursor(row_factory=dict_row) as cur:
#             cur.execute(
#                 """SELECT projects.id, projects.name, account.username FROM projects INNER JOIN people_in_projects ON projects.id = people_in_projects.project_id INNER JOIN accounts ON people_in_projects.account_id = accounts.account_id;"""
#             )
#             return cur.fetchall()

@bp.route("/", methods=["GET"])
def project_list():
    try:
        db = get_db()
        projects = get_projects(db)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return jsonify({"msg": "projects", "data": projects})

@bp.route("/", methods=["GET"])
def people_list():
    try:
        db = get_db()
        people = list_people(db)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return jsonify({"msg": "projects", "data": people})

@bp.route("/new", methods=["POST"])
def create():
    db = get_db()
    try:
        try:
            project = Project(**request.json)
        except ValidationError as e:
            return (
                jsonify(
                    {
                        "msg": "Data provided is invalid",
                        "data": e.errors(),
                        "error": "Failed to create asset from the data provided",
                    }
                ),
                400,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "msg": "Data provided is invalid",
                    "data": None,
                    "error": "Failed to create asset from the data provided",
                }
            ),
            400,
        )
    print(project)

    
    db_project = project.dict()
    with db.connection() as conn:
            res = conn.execute(
                """INSERT INTO projects (name,description)VALUES (%(name)s,%(description)s) RETURNING id;""",
                db_project,
            )
            id = res.fetchone()[0]
    for person in request.json["accountID"]:
        with db.connection() as conn:
            conn.execute(
        """INSERT INTO people_in_projects (project_id, account_id) VALUES (%(project_id)s, %(account_id)s)""",
        {"project_id" : id,
        "account_id": person}
        )

    return jsonify({"msg": "The user have created a new project"}), 200



# @bp.route("/identify", methods=["GET"])
# def identify():
#     data = decode_token(request)
#     db = get_db()
#     try:
#         if username := get_user_by_project(db, data["account_id"]):
#             username = username[0]
#     except Error as e:
#         return {"msg": str(e), "error": "Database Connection Error"}, 500

#     resp = jsonify(
#         {
#             "msg": "found you",
#             "data": {
#                 "userID": data["account_id"],
#                 "userRole": data["account_type"],
#                 "username": username,
#                 "userPrivileges": data["account_privileges"],
#             },
#         }
#     )
#     return resp

#Remove Projects from database
@bp.route("/delete/<id>", methods=["POST"])
def delete_project(id):
    database = get_db()
    canDo = True

    query = """SELECT COUNT(*) FROM people_in_projects WHERE project_id = (%(id)s);"""
    with database.connection() as conn:
        res = conn.execute(query, {"id": id})
        if (res.fetchone()[0] > 0):
            canDo = False

    query = """SELECT COUNT(*) FROM assets_in_projects WHERE project_id = (%(id)s);"""
    with database.connection() as conn:
        res = conn.execute(query, {"id": id})
        if (res.fetchone()[0] > 0):
            canDo = False

    if canDo:
        query = """DELETE FROM people_in_projects WHERE project_id = (%(id)s);"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

        query = """DELETE FROM assets_in_projects WHERE project_id = (%(id)s);"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

        query = """DELETE FROM projects WHERE id = (%(id)s);"""
        with database.connection() as conn:
            conn.execute(query, {"id": id})

    return {"msg": "", "wasAllowed": canDo}, 200

@bp.route("/allPeople", methods=["GET"])
def get_allProjects():
    database = get_db()
    query = """SELECT account_id,first_name, last_name, username FROM accounts;"""
    with database.connection() as conn:
        res = conn.execute(query)
        allPeople = res.fetchall()
        allPeople_listed = extract_people(allPeople)
        return {"data": allPeople_listed}, 200

# @bp.route("/<id>", methods=["POST"])
# def get_people_from_project(id):
#     db = get_db()
#     people = get_people(db)
#     with db.connection() as conn:
#             conn.execute(
#                 "SELECT * FROM projects WHERE id = %(id)s"
#             )
#             project = conn.fetchone()
#             if project is None:
#                 return {"msg": "Project not found"}, 404
            
#             data = decode_token(request)
#             conn.execute(
#                 "INSERT INTO people_in_projects (project_id, account_id) VALUES (%(id)s, %(account_id)s)",
#                 {"project_id": id, "account_id": data["account_id"]},
#             )
#             return {"msg": "People added to project successfully", "data": people}, 200

# @bp.route("/people/<id>", methods=["POST"])
# def add_people_to_project(id):
#     db = get_db()
#     try:
#         account_id = request.json['account_id']
#     except KeyError:
#         return jsonify(
#             {"msg": "Data provided is invalid", "data": None, "error": "Missing 'account_id' field"}
#         ), 400
    
#     with db.connection() as conn:
#         conn.execute(
#             "SELECT * FROM projects WHERE id = %(id)s",
#             {"id": id}
#         )
        
#         project = conn.fetchone()
#         if project is None:
#             return {"msg": "Project not found"}, 404
        
#         conn.execute(
#             "SELECT * FROM accounts WHERE account_id = %(account_id)s",
#             {"account_id": account_id}
#         )
#         account = conn.fetchone()
#         if account is None:
#             return {"msg": "Account not found"}, 404
        
#         try:
#             conn.execute(
#                 "INSERT INTO people_in_projects (project_id, account_id) VALUES (%(project_id)s, %(account_id)s)",
#                 {"project_id": id, "account_id": account_id}
#             )
#         except Error as e:
#             return {"msg": str(e), "error": "Database Error"}, 500
        
#         return {"msg": "People added to project successfully"}, 200

# @bp.route("/<id>/people", methods=["DELETE"])
# def remove_people_from_project(id):
#     db = get_db()
#     try:
#         account_id = request.json['account_id']
#     except KeyError:
#         return jsonify(
#             {"msg": "Data provided is invalid", "data": None, "error": "Missing 'account_id' field"}
#         ), 400
    
#     with db.connection() as conn:
#         conn.execute(
#             "SELECT * FROM projects WHERE id = %(id)s",
#             {"id": id}
#         )
#         project = conn.fetchone()
#         if project is None:
#             return {"msg": "Project not found"}, 404
        
#         conn.execute(
#             "SELECT * FROM accounts WHERE account_id = %(account_id)s",
#             {"account_id": account_id}
#         )
#         account = conn.fetchone()

#         if account is None:
#             return {"msg": "Account not found"}, 404
        
#         try:
#             conn.execute(
#                 "DELETE FROM people_in_projects WHERE project_id = %(project_id)s AND account_id = %(account_id)s",
#                 {"project_id": id, "account_id": account_id}
#             )
#         except Error as e:
#             return {"msg": str(e), "error": "Database Error"}, 500
        
#         return {"msg": "People removed from project successfully"}, 200