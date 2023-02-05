from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.db import get_db
from app.schemas import Project

bp = Blueprint("projects", __name__, url_prefix="/projects")


@bp.route("/new", methods=["POST"])
def create():
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

    db = get_db()
    db_project = Project.dict()
    with db.connection() as conn:
        conn.execute(
            """INSERT INTO project (project_id, name, description)VALUES (%(project_id)s,%(name)s,%(description)s);""", db_project,
        )
    return jsonify({"msg": "The user have created a new project"}), 200
