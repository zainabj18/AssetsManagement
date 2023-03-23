import json

from flask import Blueprint, jsonify, request
from psycopg.rows import class_row, dict_row
from pydantic import ValidationError

from app.db import get_db
from app.schemas import Project
from app.schemas.asset import AssetBaseInDB

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
        with db_conn.cursor() as cur:
            cur.execute("""SELECT * FROM projects;""")
            pList = cur.fetchall()
            allProjects = []
            for project in pList:
                allProjects.append(
                    {
                        "projectID": project[0],
                        "projectName": project[1],
                        "projectDescription": project[2],
                    }
                )
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
                "username": person[3],
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


def add_people_to_project(db, id, account_id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO people_in_projects(project_id,account_id)
            VALUES(%(project_id)s,%(account_id)s);
            """,
                {"account_id": account_id, "project_id": id},
            )


"""
Delete a person from a project.

Parameters:
db (object): The database connection object.
account_id (int): The account ID of the person to delete.
id (int): The ID of the project to remove the person from.

Returns:
None
"""


def delete_people_in_project(db, account_id, id):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            DELETE FROM people_in_projects WHERE account_id = ANY(%(account_id)s)) AND id=%(id)s;
            """,
                {"account_id": account_id, "id": id},
            )


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


"""
    Creates a new project in the database, based on the JSON data provided in the request body.

    If the data is invalid or cannot be used to create a project, returns a JSON error response with
    status code 400.

    If the project is successfully created, returns a JSON success response with status code 200.

    The JSON data should have the following keys:
    - "name": a string with the name of the project
    - "description": a string with a description of the project

    Example JSON data:
    {
        "name": "Project X",
        "description": "A project about X",
    }
"""


@bp.route("/<id>", methods=["GET"])
def get_id(id):
    db = get_db()
    query = """SELECT name, description FROM projects WHERE id=%(id)s """
    key = {"id": id}
    with db.connection() as conn:
        res = conn.execute(query, key)
        project = res.fetchall()[0]
        data = {
            "projectName": project[0],
            "projectDescription": project[1],
        }
    return {"data": data}, 200


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
        conn.execute(
            """INSERT INTO projects (name,description)VALUES (%(name)s,%(description)s)""",
            db_project,
        )

    return jsonify({"msg": "The user have created a new project"}), 200


"""
#Remove Projects from database
Delete a project with the given id from the database, along with all associated people and assets in projects.

:param id: The id of the project to be deleted.
:type id: str

:return: A dictionary containing the message indicating the success or failure of the deletion and a boolean flag indicating whether or not the deletion was allowed.
:rtype: dict
"""


@bp.route("/delete/<id>", methods=["POST"])
def delete_project_and_people(id):
    db = get_db()
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """DELETE FROM projects WHERE id = %(project_id)s;""",
                {"project_id": id},
            )

    return {"msg": ""}, 200


@bp.route("/assets/<id>", methods=["GET"])
def get_assets_in_project(id):
    query = """
    SELECT *
    FROM assets AS a
    INNER JOIN assets_in_projects as ap ON a.asset_id = ap.asset_id
    WHERE ap.project_id = %(id)s;
    """
    key = {"id": id}
    db = get_db()
    with db.connection() as conn:
        with conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute(query, key)
            assets = [json.loads(row.json(by_alias=True)) for row in cur.fetchall()]
        res = conn.execute(
            """SELECT name, description FROM projects WHERE id = %(id)s""", {"id": id}
        )
        project = res.fetchone()
        project = {"name": project[0], "description": project[1]}
    return {"data": {"assets": assets, "project": project}}, 200
