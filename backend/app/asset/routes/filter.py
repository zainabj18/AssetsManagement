from app.db import get_db
from app.schemas import FilterSearch,QueryJoin
from flask import Blueprint,request
from itertools import chain
from .. import services,utils
from app.core.utils import model_creator

bp = Blueprint("filter", __name__, url_prefix="/filter")

@bp.route("/filter", methods=["POST"])
def filter():
    """Finds all assets based on filter criteria.

    Args:
      id: The asset id to add related comment.
      user_id: The id of the user making the request.
      access_level: The access level of the user.
    
    Returns:
      A list of assets ids.
    """
    filter=model_creator(model=FilterSearch,err_msg="Failed to run filter from the data provided",**request.json)
    db = get_db()
    # the list of sets of asset ids to joint
    filter_asset_ids=[]
    
    # filter based on tags
    if filter.tag_operation==QueryJoin.OR:
        tags_results=services.fetch_assets_with_any_links(db,filter.tags,link_table="assets_in_tags",fkey="tag_id")
    else:
        tags_results=services.fetch_assets_with_set_links(db,filter.tags,link_table="assets_in_tags",fkey="tag_id")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",tags_results)))
    
    # filter based on projects
    if filter.project_operation==QueryJoin.OR:
        project_results=services.fetch_assets_with_any_links(db=db,fkeys=filter.projects,link_table="assets_in_projects",fkey="project_id")
    else:
        project_results=services.fetch_assets_with_set_links(db,filter.projects,link_table="assets_in_projects",fkey="project_id")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",project_results)))
    
    # filter based on classification
    classification_results=services.fetch_assets_with_any_values(db=db,values=filter.classifications,attribute="classification")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",classification_results)))
    
    # filter based on type
    type_results=services.fetch_assets_with_any_values(db=db,values=filter.types,attribute="version_id")
    filter_asset_ids.append(set(utils.get_key_from_results("asset_id",type_results)))
    
    # holds a list of sets of asset ids based on attribute filters
    filter_attributes_results=[]
    # iterates overs all attributes searchers
    for searcher in filter.attributes:
        # apply filter based on attribute
        filter_results=services.fetch_assets_attribute_filter(db=db,searcher=searcher)
        # unpack results of query to get asset ids and adds to interm results 
        filter_results=set(utils.get_key_from_results("asset_id",filter_results))
        filter_attributes_results.append(filter_results)
    print(filter_attributes_results)

    # join interm results  of the the attribute filter
    if filter.attribute_operation==QueryJoin.OR:
        filter_attributes_results=set(chain.from_iterable(filter_attributes_results))
    else:
        filter_attributes_results=set.intersection(*filter_attributes_results)
    filter_asset_ids.append(filter_attributes_results)

    # join all interm results based on previous searches
    if filter.operation==QueryJoin.AND:  
        asset_ids=set.intersection(*filter_asset_ids)
    else:
        asset_ids=set(chain.from_iterable(filter_asset_ids))
    return {"data": list(asset_ids)}

