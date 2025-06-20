from flask import abort,jsonify
from app.core.utils import run_query,QueryResult
from app.schemas import Comment,CommentOut,AssetOut,AttributeSearcher,QueryOperation,Log,Attribute,AssetBaseInDB,Project,AssetBaseInDB,AttributeInDB,AssetSummary
from app.db import DataAccess,Models
from psycopg.rows import class_row
from psycopg_pool import ConnectionPool
from psycopg import sql
from typing import List,Any,Union,Optional
def abort_asset_not_exists(db:ConnectionPool,asset_id:int):
    """Checks that an asset exist if not aborts.

    Args:
      db: A object for managing connections to the db.
      asset_id:The asset_id that need checking in the db.
    """
    results=run_query(db,"""SELECT asset_id FROM assets WHERE asset_id=%(id)s;""",
                {"id": asset_id},return_type=QueryResult.ONE)
    if results is None:
        abort(404,description={"msg": "Asset doesn't exist"})

def abort_insufficient(db:ConnectionPool,asset_id:int,access_level:DataAccess):
    """Checks that an asset can be viewed by account if not aborts.

    Args:
      db: A object for managing connections to the db.
      asset_id:The asset_id that need checking in the db.
    """
    results=run_query(db,"""SELECT asset_id FROM assets WHERE asset_id=%(id)s AND classification<=%(access_level)s;""",
                {"id": asset_id,"access_level":access_level},return_type=QueryResult.ONE)
    if results is None:
      abort(403)

                
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
      A list of related assets.
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



def fetch_assets_by_same_attribute(db:ConnectionPool,asset_id:int,access_level:DataAccess,related_attribute:str):
    """Find all asset with the same classification as another asset.

    Args:
      db: A object for managing connections to the db.
      asset_id: The id of the asset to compare with.
      access_level: The classification of assets the account it premited to view.
      related_attribute: The attribute that the assets must share.

    Returns:
      A list of related assets.
    """
    query=sql.SQL("""
SELECT assets.*,CONCAT(type_name,'-',version_number) AS type FROM assets
INNER JOIN type_version ON type_version.version_id=assets.version_id
INNER JOIN types ON types.type_id=type_version.type_id
WHERE assets.classification<=%(access_level)s AND assets.{attribute}=(SELECT {attribute} FROM assets WHERE asset_id=%(asset_id)s) AND asset_id!=%(asset_id)s ORDER BY asset_id;""").format(attribute=sql.Identifier(related_attribute))
    return run_query(db,query,{"asset_id": asset_id,"access_level":access_level,},return_type=QueryResult.ALL_JSON,row_factory=class_row(AssetOut))


def fetch_assets_by_link(db:ConnectionPool,asset_id:int,access_level:DataAccess,from_col:str,to_col:str):
    """Find all asset linked to an asset.

    Args:
      db: A object for managing connections to the db.
      asset_id: The id of the asset to compare with.
      access_level: The classification of assets the account it premited to view.
      from_col: The asset link going from col.
      to_col: The asset link going to col.

    Returns:
      A list of related assets.
    """
    query=sql.SQL("""
SELECT assets.*,CONCAT(type_name,'-',version_number) AS type FROM assets_in_assets
INNER JOIN assets on assets.asset_id=assets_in_assets.{from_col} 
INNER JOIN type_version ON type_version.version_id=assets.version_id
INNER JOIN types ON types.type_id=type_version.type_id
WHERE assets.classification<=%(access_level)s AND {to_col}=%(asset_id)s ORDER BY asset_id;""").format(from_col=sql.Identifier(from_col),to_col=sql.Identifier(to_col))
    return run_query(db,query,{"asset_id": asset_id,"access_level":access_level},return_type=QueryResult.ALL_JSON,row_factory=class_row(AssetOut))


def fetch_assets_with_any_links(db:ConnectionPool,fkeys:List[int],link_table:str,fkey:str):
    """Find all asset ids that has any of the given tags.

    Args:
      db: A object for managing connections to the db.
      fkeys: The list of forirgn keys  to filter by.
      link_table: The table that links assets to another table in db.
      fkey: The foreign key that used in the linking table.
    Returns:
      A list of asset ids.
    """
    query=sql.SQL("""SELECT asset_id FROM {table} WHERE {fkey}=ANY(%(fkeys)s);""""").format(table=sql.Identifier(link_table),fkey=sql.Identifier(fkey))
    return run_query(db,query,{"fkeys":fkeys},return_type=QueryResult.ALL)

def fetch_assets_with_set_links(db:ConnectionPool,fkeys:List[int],link_table:str,fkey:str):
    """Find all asset ids that has all of the given ids of a link.

    Args:
      db: A object for managing connections to the db.
      fkeys: The list of forirgn keys  to filter by.
      link_table: The table that links assets to another table in db.
      fkey: The foreign key that used in the linking table.

    Returns:
      A list of asset ids.
    """
    query=sql.SQL("""SELECT asset_id FROM assets
    WHERE %(fkeys)s::int[]<@ARRAY(SELECT {fkey} FROM {table} WHERE {table}.asset_id=assets.asset_id);""""").format(table=sql.Identifier(link_table),fkey=sql.Identifier(fkey))
    return run_query(db,query,{"fkeys":fkeys},return_type=QueryResult.ALL)

def fetch_assets_with_any_values(db:ConnectionPool,values:List[Any],attribute:str):
    """Find all asset ids that that have one of the attributes values.

    Args:
      db: A object for managing connections to the db.
      values: The possible values for the attribute.
      attribute: The attribute name.

    Returns:
      A list of asset ids.
    """
    query=sql.SQL("""SELECT DISTINCT asset_id FROM assets WHERE {attribute}=ANY(%(values)s)""""").format(attribute=sql.Identifier(attribute))
    return run_query(db,query,{"values":values},return_type=QueryResult.ALL)

def fetch_assets_attribute_filter(db:ConnectionPool,searcher:AttributeSearcher):
    """Find all asset that as attributes that support like,equal and has.

    Args:
      db: A object for managing connections to the db.
      searcher: The attribute searcher.

    Returns:
      A list of asset ids.
    """
    query=sql.Composed([sql.SQL("SELECT asset_id FROM all_atributes WHERE attribute_id=%(attribute_id)s")])
    params={"attribute_id":searcher.attribute_id}
    match searcher.operation:
      case QueryOperation.EQUALS:
          query+=sql.SQL(" AND values=%(value)s")
          params.update({"value":str(searcher.attribute_value)})
      case QueryOperation.LIKE:
          query+=sql.SQL(" AND values like %(value)s")
          params.update({"value":f"%{str(searcher.attribute_value)}%"})
      case _:
            pass
    return run_query(db,query,params,return_type=QueryResult.ALL)


def get_asset_logs(db,asset_id):
    """Find all asset logs.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset id to retrieve log.

    Returns:
      A list of logs.
    """
    return run_query(db,"""SELECT audit_logs.*, username FROM audit_logs
                INNER JOIN accounts ON accounts.account_id=audit_logs.account_id
WHERE object_id=%(asset_id)s AND model_id=%(model_id)s
ORDER BY date DESC;""",
                {"asset_id": asset_id,"model_id":int(Models.ASSETS)},return_type=QueryResult.ALL_JSON,row_factory=class_row(Log))



def add_asset_to_db(db:ConnectionPool,name:str,link:str,version_id:int,description:str,classification:Union[str,DataAccess],account_id:int,**kwargs):
    """Inserts asset into db.

    Args:
      db: A object for managing connections to the db.
      name: The name of the new asset.
      link: The link of the new asset.
      version_id: The version_id of the new asset.
      description: The description of the new asset.
      classification: The classification of the new asset.
      account_id: The account for the asset to be associated too.

    Returns:
      A dictionary containing they key asset_id.
    """
    return run_query(db,"""
            INSERT INTO assets (name,link,version_id,description, classification,account_id)
    VALUES (%(name)s,%(link)s,%(version_id)s,%(description)s,%(classification)s,%(account_id)s)  RETURNING asset_id;""",
                {"name":name,"link":link,"version_id":version_id,"description":description,"classification":classification,"account_id":account_id},return_type=QueryResult.ONE)


def update_asset(db:ConnectionPool,name:str,link:str,version_id:int,description:str,classification:Union[str,DataAccess],asset_id:int,**kwargs):
    """Updates asset in db.

    Args:
      db: A object for managing connections to the db.
      name: The name of the asset.
      link: The link of the asset.
      version_id: The version_id of the asset.
      description: The description of the asset.
      classification: The classification of the asset.
      asset_id: The asset id to update.

    Returns:
      A dictionary containing they key asset_id.
    """
    return run_query(db,"""
    UPDATE assets 
SET name=%(name)s,link=%(link)s,description=%(description)s,version_id=%(version_id)s,classification=%(classification)s,last_modified_at=now() WHERE asset_id=%(asset_id)s ;""",
                {"name":name,"link":link,"version_id":version_id,"description":description,"classification":classification,"asset_id":asset_id})


def fetch_version_dependencies(db:ConnectionPool,version_id:int):
    """Find the version's dependencies.

    Args:
      db: A object for managing connections to the db.
      version_id: The version id to check dependencies.

    Returns:
      A list of dictionaries containing version id and concatenated type name.
    """
    return run_query(db,"""SELECT type_version_to as version_id,CONCAT(type_name,'-',version_number) AS type_name  FROM type_version_link
INNER JOIN type_version ON type_version.version_id=type_version_link.type_version_to
INNER JOIN types ON types.type_id=type_version.type_id WHERE type_version_from=%(version_id)s;""",{"version_id":version_id},return_type=QueryResult.ALL)



def fetch_assets_versions(db:ConnectionPool,assets_ids:List[int]):
    """Find the version ids of a list of assets ids.

    Args:
      db: A object for managing connections to the db.
      assets_ids: The list asset ids versions to find.

    Returns:
      A list of dictionaries containing version id.
    """
    return run_query(db,"""SELECT version_id FROM assets WHERE asset_id=ANY(%(asset_ids)s);""",{"asset_ids":assets_ids},return_type=QueryResult.ALL)

def fetch_attributes_by_version(db:ConnectionPool,version_id:int,required=False):
    """Find the attributes related to a version.

    Args:
      db: A object for managing connections to the db.
      version_id: The type version id to get the attributes.
      required: A boolean if to only include required ones.

    Returns:
      A list of dictionaries containing keys attribute_id and attribute_name.
    """
    query=sql.Composed([sql.SQL("""SELECT attributes_in_types.attribute_id,attributes.attribute_name FROM attributes_in_types
INNER JOIN attributes on attributes_in_types.attribute_id=attributes.attribute_id
WHERE attributes_in_types.type_version=%(version_id)s""")])
    if required:
        query+=sql.SQL(" AND (attributes.validation_data->>'isOptional')::boolean is false;")
    return run_query(db,query,{"version_id":version_id},return_type=QueryResult.ALL)


def add_asset_tags_to_db(db:ConnectionPool,asset_id:int,tags:List[int]):
    """Inserts asset's tags into db.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset's id to add.
      tags: A list of tag ids.
    """
    for tag in tags:
        run_query(db,"""
                INSERT INTO assets_in_tags (asset_id,tag_id)
        VALUES (%(asset_id)s,%(tag_id)s) ON CONFLICT DO NOTHING;""",
                    {"asset_id": asset_id, "tag_id": tag})
        
def add_asset_projects_to_db(db:ConnectionPool,asset_id:int,projects:List[int]):
    """Inserts asset's projects into db.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset's id to add.
      projects: A list of project ids.
    """
    for project in projects:
        run_query(db, """
                INSERT INTO assets_in_projects (asset_id,project_id)
        VALUES (%(asset_id)s,%(project_id)s) ON CONFLICT DO NOTHING;""",
                    {"asset_id": asset_id, "project_id": project}
                )

def add_asset_assets_to_db(db:ConnectionPool,asset_id:int,assets:List[int]):
    """Inserts asset's assets into db.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset's id to add.
      assets: A list of asset ids.
    """
    for asset in assets:
        run_query(db,  """
                INSERT INTO assets_in_assets (from_asset_id,to_asset_id)
        VALUES (%(from_asset_id)s,%(to_asset_id)s) ON CONFLICT DO NOTHING;""",
                    {"from_asset_id": asset_id, "to_asset_id": asset})

def add_asset_metadata_to_db(db:ConnectionPool,asset_id:int,metadata:List[Attribute]):
    """Inserts asset's assets into db.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset's id to add.
      metadata: A list of attributes to add to the db.
    """
    for attribute in metadata:
        run_query(db,"""
                INSERT INTO attributes_values (asset_id,attribute_id,attribute_value)
        VALUES (%(asset_id)s,%(attribute_id)s,%(value)s) ON CONFLICT (asset_id,attribute_id) DO UPDATE SET attribute_value = EXCLUDED.attribute_value;""",
                    {
                        "asset_id": asset_id,
                        "attribute_id": attribute.attribute_id,
                        "value": attribute.attribute_value,
                    },
                )
         
def fetch_asset(db:ConnectionPool,asset_id:int):
    """Fetches an asset's with all its metadata and attributes from db.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset's id to fetch.
    """
    return run_query(db, """SELECT * FROM assets_out WHERE asset_id=%(asset_id)s""",
                    {"asset_id": asset_id},row_factory=class_row(AssetOut),return_type=QueryResult.ONE)

def fetch_asset_flattend(db:ConnectionPool,asset_id:int):
    """Fetches an asset's with all its project_ids,asset_ids,metadata and attributesfrom db.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset's id to fetch.
    """
    return run_query(db, """SELECT * FROM flatten_assets WHERE asset_id=%(asset_id)s""",
                    {"asset_id": asset_id},row_factory=class_row(AssetOut),return_type=QueryResult.ONE)

def fetch_assets_summary(db:ConnectionPool,classification:DataAccess,account_id=None):
    """Fetches all asset's from db.

    Args:
      db: A object for managing connections to the db.
      classification: The max classification level to view.
    """
    query=sql.Composed([sql.SQL("""SELECT assets.*,type_names_versions.type_name FROM assets
INNER JOIN type_names_versions ON type_names_versions.version_id=assets.version_id 
WHERE classification<=%(classification)s""")])
    if account_id is not None:
        query+=sql.SQL(" AND account_id =%(account_id)s")
    query+=sql.SQL(" ORDER BY asset_id")

    return run_query(db,query,
                    {"classification": classification,"account_id":account_id},row_factory=class_row(AssetBaseInDB),return_type=QueryResult.ALL_JSON)
             
      


def fetch_assets_projects_selected(db:ConnectionPool,asset_id:int):
    """Fetches all projects from db with asset's projects row as is_selected True.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset id to get projects for.
    """
    return run_query(db, """
                SELECT projects.*,
CASE WHEN id in (SELECT project_id FROM assets_in_projects WHERE asset_id=%(asset_id)s) 
THEN 'TRUE' else 'FALSE' end as is_selected  FROM projects ORDER BY is_selected DESC;""",
                    {"asset_id": asset_id},row_factory=class_row(Project),return_type=QueryResult.ALL_JSON)


def fetch_assets_asssets_selected(db:ConnectionPool,asset_id:int,classification:DataAccess):
    """Fetches all assets from db with asset's assets row as is_selected True.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset id to get assets for.
      classification: The max classification level to view.
    """
    return run_query(db, """
    SELECT assets.*,
CASE WHEN asset_id in (SELECT to_asset_id FROM assets_in_assets WHERE from_asset_id=%(asset_id)s)
THEN 'TRUE' else 'FALSE' end as is_selected FROM assets 
WHERE asset_id!=%(asset_id)s AND classification<=%(classification)s;""",
                    {"asset_id": asset_id,"classification":classification},row_factory=class_row(AssetBaseInDB),return_type=QueryResult.ALL_JSON)


def fetch_asset_current_and_max_versions(db:ConnectionPool,asset_id:int):
    """Fetches assets current and max verison for type.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset id to get versions for.
    """
    return run_query(db, """WITH max_versions AS (
SELECT version_id,MAX (version_id) OVER (PARTITION BY type_id) as max_version_id FROM type_version)
SELECT max_versions.* FROM max_versions
INNER JOIN assets ON assets.version_id=max_versions.version_id
WHERE asset_id=%(asset_id)s;""",
                    {"asset_id": asset_id},return_type=QueryResult.ONE)

def fetch_versions_attributes(db:ConnectionPool,version_id:int):
    """Fetches a versions attributes.

    Args:
      db: A object for managing connections to the db.
      version_id: The version id attributes to be fetched.
    """
    return run_query(db, """SELECT attributes.* FROM attributes_in_types 
        INNER JOIN attributes ON attributes.attribute_id=attributes_in_types.attribute_id
        WHERE type_version=%(type_version)s;""",{"type_version":version_id},return_type=QueryResult.ALL_JSON,row_factory=class_row(AttributeInDB))


def delete_projects_from_asset(db:ConnectionPool,asset_id:int,projects:Optional[List[int]]=None):
    """Deletes the realtionship between projects and an asset.

    Args:
      db: A object for managing connections to the db.
      projects: The list of projects to deleted.
      asset_id: The asset id to remove the projects from.
    """
    query=sql.Composed([sql.SQL("""DELETE FROM assets_in_projects WHERE asset_id=%(asset_id)s""")])
    if projects is not None:
        query+=sql.SQL(" AND project_id = ANY(%(project_ids)s);")
    return run_query(db,query,{"project_ids":projects,"asset_id":asset_id})

def delete_tags_from_asset(db:ConnectionPool,asset_id:int,tags:Optional[List[int]]=None):
    """Deletes the realtionship between tags and an asset.

    Args:
      db: A object for managing connections to the db.
      tags: The list of tags to deleted.
      asset_id: The asset id to remove the tags from.
    """
    query=sql.Composed([sql.SQL("""DELETE FROM assets_in_tags WHERE asset_id=%(asset_id)s""")])
    if tags is not None:
        query+=sql.SQL(" AND tag_id = ANY(%(tag_ids)s);")
    return run_query(db,query,{"tag_ids":tags,"asset_id":asset_id})

def delete_attributes_from_asset(db:ConnectionPool,asset_id:int,attributes:Optional[List[int]]=None):
    """Deletes the realtionship between attributes and an asset.

    Args:
      db: A object for managing connections to the db.
      attributes: The list of attributes ids to deleted.
      asset_id: The asset id to remove the attributes from.
    """
    query=sql.Composed([sql.SQL("""DELETE FROM attributes_values WHERE asset_id=%(asset_id)s""")])
    if attributes is not None:
        query+=sql.SQL(" AND attribute_id = ANY(%(attributes)s);")
    return run_query(db,query,{"attributes":attributes,"asset_id":asset_id})


def delete_assets_from_asset(db:ConnectionPool,asset_id:int,asset_ids:Optional[List[int]]=None):
    """Deletes the realtionship between assets and an asset.

    Args:
      db: A object for managing connections to the db.
      asset_ids: The list of assets ids to deleted.
      asset_id: The asset id to remove the assets from.
    """
    query=sql.Composed([sql.SQL("""DELETE FROM assets_in_assets WHERE from_asset_id=%(asset_id)s""")])
    if asset_ids is not None:
        query+=sql.SQL(" AND to_asset_id = ANY(%(asset_ids)s);")
    return run_query(db,query,{"asset_ids":asset_ids,"asset_id":asset_id})

def delete_asset(db:ConnectionPool,asset_id:int):
    """Deletes an asset from db.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset id to delete.
    """
    return run_query(db,"""DELETE FROM assets WHERE asset_id=%(asset_id)s""",{"asset_id":asset_id})

def fetch_asset_dependencies(db:ConnectionPool,asset_id:int):
    """Finds all asset depene.

    Args:
      db: A object for managing connections to the db.
      asset_id: The asset id to check the dependecnies for.
    """
    return run_query(db,"""SELECT asset_id,name FROM assets_in_assets
INNER JOIN assets ON assets_in_assets.from_asset_id=assets.asset_id
WHERE to_asset_id=%(asset_id)s""",{"asset_id":asset_id},row_factory=class_row(AssetSummary),return_type=QueryResult.ALL_JSON)