from flask import abort,jsonify
from app.core.utils import run_query,QueryResult
from app.schemas import TagBase,Comment,CommentOut,AssetOut,AttributeSearcher,QueryOperation,Log,Attribute,AssetBaseInDB,Project,AssetBaseInDB,AttributeInDB,AssetSummary
from app.db import DataAccess,Models
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg import sql
from typing import List,Any,Union,Optional

def tag_in_db(db:ConnectionPool,tag_id:int,abort=True):
    """Checks that an tags exist if not aborts.

    Args:
      db: A object for managing connections to the db.
      tag_id:The tag_id that need checking in the db.
      abort: Aborts when tag not found
    """
    res=run_query(db, """SELECT id FROM tags WHERE id=%(id)s""",{"id":tag_id},return_type=QueryResult.ONE)
    if res is None and abort:
        abort(404,description={"msg": "Asset doesn't exist"})
    return not res is None

def create_tag(db, tag_dict):
    with db.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
        INSERT INTO tags (name)
VALUES (%(name)s) RETURNING id;""",
                tag_dict,
            )
            return cur.fetchone()[0]

                
def insert_tag_to_db(db:ConnectionPool,tag:TagBase):
    """Add a new tag to db.

    Args:
      db: A object for managing connections to the db.
      tag: An object represnetation of the tag.
    """
    print(tag)
    return run_query(db, """
        INSERT INTO tags (name) VALUES (%(name)s) RETURNING id;""",{"name":tag.name},return_type=QueryResult.ONE)

def list_tags(db:ConnectionPool):
    """Fetches all tags in db.

    Args:
      db: A object for managing connections to the db.
    """
    return run_query(db, """SELECT * FROM tags ORDER BY name;""",return_type=QueryResult.ALL)

def delete_tag(db:ConnectionPool,tag_id:int):
    """Deletes a tag.

    Args:
      db: A object for managing connections to the db.
      tag_id: The id of the tag to delete.
    """
    return run_query(db,"""DELETE FROM tags WHERE id=%(id)s;""",
                {"id": tag_id})


def update_tag(db:ConnectionPool,tag:TagBase):
    """Updates a tag.

    Args:
      db: A object for managing connections to the db.
      tag: An object represnetation of the tag.
    """
    return run_query(db,
                """
            UPDATE tags 
            SET name=%(name)s WHERE id=%(id)s ;""",
                tag.dict(),
            )

def add_asset_to_tag(db:ConnectionPool,asset_ids:List[int],tag_id:int):
    """Updates a tag assets.

    Args:
      db: A object for managing connections to the db.
      asset_ids: The list of asset ids to add to tag.
      tag_id: The tag id to add to.
    """
    return run_query(db,"""
            INSERT INTO assets_in_tags(asset_id,tag_id)
SELECT asset_id,%(tag_id)s AS tag_id FROM assets
WHERE asset_id = ANY(%(asset_ids)s) ON CONFLICT DO NOTHING;
            """,{"tag_id":tag_id,"asset_ids":asset_ids})

def delete_asset_in_tag(db:ConnectionPool,asset_ids:List[int],tag_id:int):
    """Removes a tag assets.

    Args:
      db: A object for managing connections to the db.
      asset_ids: The list of asset ids to from form tag.
      tag_id: The tag id to remove from.
    """
    return run_query(db,"""
            DELETE FROM assets_in_tags WHERE asset_id = ANY(%(asset_ids)s) AND tag_id=%(tag_id)s;
            """,{"tag_id":tag_id,"asset_ids":asset_ids})

def fetch_assets_in_tag(db:ConnectionPool,tag_id:int):
    """Fetches assets in tags.

    Args:
      db: A object for managing connections to the db.
      tag_id: The tag id to get the assets for.
    """
    return run_query(db,"""SELECT * FROM flatten_assets WHERE %(tag_id)s=ANY(flatten_assets.tag_ids) ORDER BY asset_id;""",
                {"tag_id": tag_id},row_factory=class_row(AssetOut),return_type=QueryResult.ALL_JSON)


def fetch_tag_name(db:ConnectionPool,tag_id:int):
    """Fetches a tassets in tags.

    Args:
      db: A object for managing connections to the db.
      tag_id: The tag id to fetch.
    """
    return run_query(db,"""SELECT name FROM tags WHERE id=%(tag_id)s;""",
                {"tag_id": tag_id},return_type=QueryResult.ONE)
