from flask import Blueprint, jsonify
from psycopg import Error
from psycopg.rows import dict_row

from app.db import get_db

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
