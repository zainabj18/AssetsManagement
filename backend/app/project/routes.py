import json
from app.db import get_db
from app.schemas import Project
from flask import Blueprint, jsonify, request
from psycopg import Error
from psycopg.rows import dict_row
from pydantic import ValidationError

bp = Blueprint("project", __name__, url_prefix="/project")


def get_projects(db):
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM projects;""")
            query = """SELECT id, name, description FROM projects"""
            with db.connection() as conn:
                res = conn.execute(query)
                pList = res.fetchall()
            allProjects = []
            for project in pList:
                query = """SELECT username, accounts.account_id
                FROM people_in_projects
                INNER JOIN accounts ON accounts.account_id = people_in_projects.account_id
                WHERE project_id = %(project_id)s;"""
                key = {"project_id":project[0]}
                res = db_conn.execute(query, key)
                people = res.fetchall()
                accounts = []
                for account in people:
                    accounts.append({"username": account[0], "account_id": account[1]})
                allProjects.append({
                    "projectID": project[0],
                    "projectName":project[1],
                    "projectDescription":project[2],
                    "accounts": accounts
                })
    return allProjects

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

"""
Get a list of all projects in the database, along with the people associated with each project.

Args:
db (obj): The database object to execute the SQL queries.

Returns:
A list of dictionaries, where each dictionary represents a project and contains the following keys:
- "projectID": An integer representing the project's unique identifier.
- "projectName": A string representing the project's name.
- "projectDescription": A string representing the project's description.
- "accounts": A list of dictionaries, where each dictionary contains the following keys:
- "username": A string representing the associated person's username.
- "account_id": An integer representing the associated person's unique identifier.
"""
@bp.route("/", methods=["GET"])
def people_list():
    db = get_db()
    data = get_projects(db)
    return {"msg": "projects", "data": data}

"""
    Creates a new project in the database, based on the JSON data provided in the request body.

    If the data is invalid or cannot be used to create a project, returns a JSON error response with
    status code 400.

    If the project is successfully created, returns a JSON success response with status code 200.

    The JSON data should have the following keys:
    - "name": a string with the name of the project
    - "description": a string with a description of the project
    - "accounts": a list of integers representing the account IDs of the people involved in the project

    Example JSON data:
    {
        "name": "Project X",
        "description": "A project about X",
        "accounts": [1, 2, 3]
    }
"""

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

    
    db_project = project.dict()
    with db.connection() as conn:
            res = conn.execute(
                """INSERT INTO projects (name,description)VALUES (%(name)s,%(description)s) RETURNING id;""",
                db_project,
            )
            id = res.fetchone()[0]
    for person in request.json["accounts"]:
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

"""
Delete a project with the given id from the database, along with all associated people and assets in projects.

:param id: The id of the project to be deleted.
:type id: str

:return: A dictionary containing the message indicating the success or failure of the deletion and a boolean flag indicating whether or not the deletion was allowed.
:rtype: dict
"""

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

"""
Return a list of all people in the database.

Returns:
    A dictionary containing a list of dictionaries representing all people in the database.
    Each dictionary in the list contains keys for 'id', 'first_name', 'last_name', and 'username'.
    If the query is successful, a status code of 200 is returned.
"""

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