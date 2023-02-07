from flask import Blueprint, jsonify
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
    db = get_db()
    return jsonify({"msg": "projects","data":get_projects(db)})
