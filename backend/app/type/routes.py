from flask import Blueprint
from psycopg.rows import dict_row
from app.db import get_db

def get_types(db):
    with db.connection() as db_conn:
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM types;""")
            return cur.fetchall()
bp = Blueprint("type", __name__, url_prefix="/type")
@bp.route("/adder", methods=["GET"])
def types():
    return {"msg": ""}, 200

@bp.route("/", methods=["GET"])
def list():
    db = get_db()
    return {"msg": "types","data":get_types(db)}, 200