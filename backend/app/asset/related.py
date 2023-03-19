from flask import Blueprint
from app.core.utils import protected
from app.db import UserRole, get_db,DataAccess
from .services import fetch_assets_by_common_count_count,fetch_assets_by_same_attribute,fetch_assets_by_link
bp = Blueprint("related", __name__, url_prefix="/related")

@bp.route("/tags/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_by_tags(id:int,user_id:int, access_level:DataAccess):
    """Finds assets that share the same tags.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets.
    """
    db = get_db()
    return {"data": fetch_assets_by_common_count_count(db=db,asset_id=id,access_level=access_level,related_table="assets_in_tags",related_table_id="tag_id")}


@bp.route("/projects/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_by_projects(id:int,user_id:int, access_level:DataAccess):
    """Finds assets that share the same projects.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets.
    """
    db = get_db()
    return {"data": fetch_assets_by_common_count_count(db=db,asset_id=id,access_level=access_level,related_table="assets_in_projects",related_table_id="project_id")}

@bp.route("/classification/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_by_classification(id:int,user_id:int, access_level:DataAccess):
    """Finds assets that share the same classification.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets.
    """
    db = get_db()
    return {"data": fetch_assets_by_same_attribute(db=db,asset_id=id,access_level=access_level,related_attribute="classification")}

@bp.route("/type/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_by_type(id:int,user_id:int, access_level:DataAccess):
    """Finds assets that share the same type.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets.
    """
    db = get_db()
    return {"data": fetch_assets_by_same_attribute(db=db,asset_id=id,access_level=access_level,related_attribute="version_id")}



@bp.route("/outgoing/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_outgoing_links(id:int,user_id:int, access_level:DataAccess):
    """Finds all assets outgoging links to an asset.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets.
    """
    db = get_db()
    return {"data": fetch_assets_by_link(db=db,asset_id=id,access_level=access_level,to_col="from_asset_id",from_col="to_asset_id")}



@bp.route("/incomming/<id>", methods=["GET"])
@protected(role=UserRole.VIEWER)
def fetch_related_incomming_links(id:int,user_id:int, access_level:DataAccess):
    """Finds all assets incomming links to an asset.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets.
    """
    db = get_db()
    return {"data": fetch_assets_by_link(db=db,asset_id=id,access_level=access_level,from_col="from_asset_id",to_col="to_asset_id")}