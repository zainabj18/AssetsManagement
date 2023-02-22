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
            return cur.fetchall()


@bp.route("/", methods=["GET"])
def list():
    try:
        db = get_db()
        projects = get_projects(db)
    except Error as e:
        return {"msg": str(e), "error": "Database Error"}, 500
    return jsonify({"msg": "projects", "data": projects})


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
