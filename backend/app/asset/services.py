from flask import abort,jsonify
from app.core.utils import run_query,QueryResult
from app.schemas import Comment,CommentOut
from psycopg.rows import class_row
def abort_asset_not_exists(db,id):
    with db.connection() as db_conn:
        with db_conn.cursor() as cur:
            cur.execute(
                """SELECT asset_id FROM assets WHERE asset_id=%(id)s AND soft_delete=0;""",
                {"id": id},
            )
            if cur.fetchone() is None:
                res=jsonify({"msg": "Asset doesn't exist",
      
                "data": []
            })
                res.status_code=400
                abort(res)

def insert_comment_to_db(db,comment:Comment,account_id,asset_id):
    return run_query(db,"""INSERT INTO comments(asset_id,account_id,comment)
                 VALUES(%(asset_id)s,%(account_id)s,%(comment)s);""",{"asset_id": asset_id,"account_id":account_id,"comment":comment.comment})
def delete_comment_db(db,comment_id):
    return run_query(db,"""DELETE FROM comments WHERE comment_id = %(comment_id)s;""",{"comment_id": comment_id})

def fetch_asset_comments(db,asset_id):
    return run_query(db,"""
    SELECT comments.*,username FROM comments
INNER JOIN accounts ON accounts.account_id=comments.account_id
    WHERE asset_id=%(asset_id)s ORDER BY datetime;""",{"asset_id": asset_id},return_type=QueryResult.ALL_JSON,row_factory=class_row(CommentOut))

