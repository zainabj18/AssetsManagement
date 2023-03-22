import json
from app.db import get_db
from app.schemas import Project
from flask import Blueprint, jsonify, request
from psycopg.rows import dict_row
from pydantic import ValidationError

bp = Blueprint("project", __name__, url_prefix="/project")

"""
This function retrieves all the projects from the database along with their corresponding accounts, and returns them in a list format.

Args:
db (object): The database object that represents the connection to the database.

Returns:
list: A list of dictionaries where each dictionary represents a project.
"""
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


"""
Returns dictionaries containing information about each person in the input list of people.

Parameters:
people: A list of tuples containing information about each person.

Returns:
allPeople_listed: A list of dictionaries, where each dictionary represents a person and their information.
The dictionary has the following keys:
    - accountID: The unique account ID of the person.
    - firstName: The first name of the person.
    - lastName: The last name of the person.
    - username: The username of the person.
"""
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

"""
Adds a person to a project in the database.

Parameters:
db (DatabaseConnection): An instance of the database connection object.
id (int): The ID of the project.
account_id (int): The ID of the person to add to the project.

Returns:
None
"""
def add_people_to_project(db,id,account_id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO people_in_projects(project_id,account_id)
            VALUES(%(project_id)s,%(account_id)s);
            """,{"account_id":account_id,"project_id":id})

"""
Delete a person from a project.

Parameters:
db (object): The database connection object.
account_id (int): The account ID of the person to delete.
id (int): The ID of the project to remove the person from.

Returns:
None
"""
def delete_people_in_project(db,account_id,id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM people_in_projects WHERE account_id = ANY(%(account_id)s)) AND id=%(id)s;
            """,{"account_id":account_id,"id":id})
            

"""
Returns a list of all people associated with projects in the database.

Parameters:
db: The database instance.

Returns:
A list of dictionaries containing the account_id of each person associated with projects in the database.
"""
def list_people(db):
    with db.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT account_id FROM people_in_projects;""")
            return cur.fetchall()

"""
This function handles the GET request for the '/people' endpoint, which returns a list of projects from the database.
It calls the 'get_projects' function to retrieve the data from the database and returns it in JSON format.

Returns:
A dictionary in JSON format containing a message indicating success and a list of project data.
"""
@bp.route("/", methods=["GET"])
def people_list():
    db = get_db()
    data = get_projects(db)
    return {"msg": "projects", "data": data}

@bp.route ("/<id>", methods=["GET"])
def get_id(id):
    db = get_db()
    query = """SELECT name, description, type FROM projects WHERE id=%(id)s """
    key = {"id": id}
    with db.connection() as conn:
       res = conn.execute(query,key)
       project = res.fetchall()[0]
       data = {
                    "projectName":project[0],
                    "projectDescription":project[1],
                    "projectType": project[2]
                }
    return {"data": data}, 200

@bp.route ("/changeProjects", methods=["POST"])
def change_project():
    js = request.json
    db = get_db()
    query = """DELETE FROM people_in_projects WHERE project_id=%(project_id)s """
    key = {"project_id": js["id"]}
    with db.connection() as conn:
       conn.execute(query,key)
    if (js["private"]):
        query = """INSERT INTO people_in_projects (project_id, account_id) VALUES (%(project_id)s, %(account_id)s)"""
        for person_id in  js['selectedPeople'] :
            key = {"project_id": person_id,"account_id": js["id"]}
    
    
    return{"msg": ""}, 200

"""
Creates a new project with the data provided in the POST request and inserts it into the database.
Also inserts the associated accounts into the people_in_projects table.

Returns:
JSON response: {"msg": "The user have created a new project"} with HTTP status code 200 on success.
JSON response: {"msg": "Data provided is invalid", "data": e.errors(), "error": "Failed to create asset from the data provided"} with HTTP status code 400 on validation error.
JSON response: {"msg": "Data provided is invalid", "data": None, "error": "Failed to create asset from the data provided"} with HTTP status code 400 on other exceptions.
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



#Remove Projects from database
# @bp.route("/delete/<id>", methods=["POST"])
# def delete_project(id):
#     database = get_db()
#     canDo = True

#     query = """SELECT COUNT(*) FROM people_in_projects WHERE project_id = (%(id)s);"""
#     with database.connection() as conn:
#         res = conn.execute(query, {"project_id": id})
#         if (res.fetchone()[0] > 0):
#             canDo = False

#     query = """SELECT COUNT(*) FROM assets_in_projects WHERE project_id = (%(id)s);"""
#     with database.connection() as conn:
#         res = conn.execute(query, {"project_id": id})
#         if (res.fetchone()[0] > 0):
#             canDo = False

#     if canDo:
#         query = """DELETE FROM people_in_projects WHERE project_id = (%(id)s);"""
#         with database.connection() as conn:
#             conn.execute(query, {"project_id": id})

#         query = """DELETE FROM assets_in_projects WHERE project_id = (%(id)s);"""
#         with database.connection() as conn:
#             conn.execute(query, {"project_id": id})

#         query = """DELETE FROM projects WHERE id = (%(id)s);"""
#         with database.connection() as conn:
#             conn.execute(query, {"id": id})

#         # query = """DELETE FROM accounts WHERE account_id = (%(id)s);"""
#         # with database.connection() as conn:
#         #     conn.execute(query, {"account_id": id})

#         # delete_people_in_project(database,id,id)    

#     return {"msg": "", "wasAllowed": canDo}, 200

"""
This function deletes a project with the given id and all associated people from the database.

Parameters:
id (str): the id of the project to be deleted

Returns:
A dictionary containing a message and a boolean indicating whether the deletion was allowed.
"""
@bp.route("/delete/<id>", methods=["POST"])
def delete_project_and_people(id):
    db = get_db()
    canDo = True
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """DELETE FROM people_in_projects WHERE project_id = %(project_id)s;""",
                {"project_id": id},
            )

            cur.execute(
                """DELETE FROM projects WHERE id = %(project_id)s;""",
                {"project_id": id},
            )

    return {"msg": "", "wasAllowed": canDo}, 200

"""
Route function that handles deleting a person's account and removing them from any associated projects.

Args:
    id (str): The ID of the person whose account is to be deleted.

Returns:
    dict: A dictionary containing the message and whether the action was allowed or not.
"""
@bp.route("/delete/people/<id>", methods=["POST"])
def delete_people(id):
    db = get_db()
    canDo = True
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """DELETE FROM people_in_projects WHERE account_id = %(account_id)s;""",
                {"account_id": id},
            )

            cur.execute(
                """DELETE FROM accounts WHERE account_id = %(account_id)s;""",
                {"account_id": id},
            )

    return {"msg": "", "wasAllowed": canDo}, 200
"""
This function defines a route for getting all people in the system. It extracts data from the accounts table and returns a JSON object with a list of all the people's information including their account ID, first name, last name, and username.

Returns:
A JSON object containing a list of dictionaries, each representing a person in the system.
Each dictionary contains the person's account ID, first name, last name, and username.
A status code of 200 to indicate success.

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
