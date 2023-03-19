from flask import abort,jsonify
from app.core.utils import run_query,QueryResult
from app.schemas import Comment,CommentOut,AssetOut
from app.db import DataAccess
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg import sql
def abort_asset_not_exists(db,asset_id):
    """Checks that an asset exist if not aborts.

    Args:
      db: A object for managing connections to the db.
      asset_id:The asset_id that need checking in the db.
    """
    with db.connection() as db_conn:
        with db_conn.cursor() as cur:
            cur.execute(
                """SELECT asset_id FROM assets WHERE asset_id=%(id)s AND soft_delete=0;""",
                {"id": asset_id},
            )
            if cur.fetchone() is None:
                res=jsonify({"msg": "Asset doesn't exist",
      
                "data": []
            })
                res.status_code=400
                abort(res)

def insert_comment_to_db(db:ConnectionPool,comment:Comment,account_id:int,asset_id:int):
    """Add a new comment to db.

    Args:
      db: A object for managing connections to the db.
      comment: An object represnetation of the comment
      account_id: The account_id for who is making the comment.
      asset_id:The asset_id for the asset that a comment is being made against.
    """
    return run_query(db,"""INSERT INTO comments(asset_id,account_id,comment)
                 VALUES(%(asset_id)s,%(account_id)s,%(comment)s);""",{"asset_id": asset_id,"account_id":account_id,"comment":comment.comment})
def delete_comment_db(db,comment_id):
    """Delete a comment from the db.

    Args:
      db: A object for managing connections to the db.
      comment_id: The id of the comment to be deleted.
    """
    run_query(db,"""DELETE FROM comments WHERE comment_id = %(comment_id)s;""",{"comment_id": comment_id})

def fetch_asset_comments(db,asset_id):
    """Find all comments related to an asset.

    Args:
      db: A object for managing connections to the db.
      asset_id: The id of the asset whoses comments are needed.
    
    Returns:
      A list of comments as dicts for an asset.
    """
    return run_query(db,"""
    SELECT comments.*,username FROM comments
INNER JOIN accounts ON accounts.account_id=comments.account_id
    WHERE asset_id=%(asset_id)s ORDER BY datetime;""",{"asset_id": asset_id},return_type=QueryResult.ALL_JSON,row_factory=class_row(CommentOut))



def fetch_assets_by_common_count_count(db:ConnectionPool,asset_id:int,access_level:DataAccess,related_table:str,related_table_id:str):
    """Find all asset related to another model and count models in common with other assets.

    Args:
      db: A object for managing connections to the db.
      asset_id: The id of the asset to compare with.
      access_level: The classification of assets the account it premited to view.
      related_table: The able that links assets to another table in db.
      related_table_id: The foreign key that used in the linking table.

    Returns:
      A list of comments as dicts for an asset.
    """
    query=sql.SQL("""WITH related_asset as (SELECT COUNT(asset_id),asset_id FROM {table} WHERE {fkey} in (SELECT {fkey} FROM {table} WHERE asset_id=%(asset_id)s) and asset_id !=%(asset_id)s
GROUP BY asset_id
HAVING COUNT(asset_id)>0)
SELECT assets.*,related_asset.count,CONCAT(type_name,'-',version_number) AS type FROM assets
INNER JOIN related_asset ON assets.asset_id=related_asset.asset_id
INNER JOIN type_version ON type_version.version_id=assets.version_id
INNER JOIN types ON types.type_id=type_version.type_id
WHERE assets.classification<=%(access_level)s
ORDER BY count DESC;""").format(table=sql.Identifier(related_table),fkey=sql.Identifier(related_table_id))
    return run_query(db,query,{"asset_id": asset_id,"access_level":access_level,"related_table_id":related_table_id},return_type=QueryResult.ALL_JSON,row_factory=class_row(AssetOut))

