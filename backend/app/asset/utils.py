from . import services
import json 
from psycopg_pool import ConnectionPool
from app.schemas import Attribute,Asset,Diff
from typing import List
from flask import abort
from app.core.utils import model_creator

def can_view_asset(db,asset_id,access_level):
    services.abort_asset_not_exists(db=db,asset_id=asset_id)
    services.abort_insufficient(db=db,access_level=access_level,asset_id=asset_id)
def get_key_from_results(key,results):
    return [row[key] for row in results]

def check_asset_dependencies(db:ConnectionPool,version_id:int,assets:List[int]):
    asset_versions=services.fetch_assets_versions(db=db,assets_ids=assets)
    asset_types=set(get_key_from_results("version_id",asset_versions))
    dependents=services.fetch_version_dependencies(db=db,version_id=version_id)
    if not asset_types.issuperset(set(get_key_from_results("version_id",dependents))):
        abort(400, {"msg": "Missing dependencies", "data": get_key_from_results("type_name",dependents)})

def check_asset_metatadata(db:ConnectionPool,version_id:int,metadata:List[Attribute]):
    required_attributes=services.fetch_attributes_by_version(db=db,version_id=version_id,required=True)
    attribute_ids=set([attribute.attribute_id for attribute in metadata])
    required_attributes_names=[row["attribute_name"] for row in required_attributes]
    if not set([row["attribute_id"] for row in required_attributes]).issubset(attribute_ids):
        abort(400, {
                "msg": "Missing required attributes",
                "data":[f"Must inlcude the following attrubutes {required_attributes_names}"],
            })
    all_type_attributes=services.fetch_attributes_by_version(db=db,version_id=version_id)
    all_type_attributes_names=[row["attribute_name"] for row in required_attributes]
    if not (attribute_ids.issubset([row["attribute_id"] for row in all_type_attributes])):
        abort(400,  {
                "msg": "Addtional attributes",
                "data": [f"Must only inlcude the following attrubutes {all_type_attributes_names}"],
            })
def asset_differ(orginal,new):
    removed=list(set(orginal.keys())-set(new.keys()))
    changed=[]
    added=list(set(new.keys())-set(orginal.keys()))
    for key in orginal:
        if key in new:
            if key=="metadata":
                old_values_dict={}
                new_values_dict={}
                for at in orginal["metadata"]:
                    old_values_dict[at["attributeID"]]=at
                for at in new["metadata"]:
                    new_values_dict[at["attributeID"]]=at
                metadata_removed=list(set(old_values_dict.keys())-set(new_values_dict.keys()))
                metadata_added=list(set(new_values_dict.keys())-set(old_values_dict.keys()))
                for attribute in metadata_removed:
                    name=old_values_dict[attribute]["attributeName"]
                    removed.append(f"metadata-{attribute}-{name}")
                for attribute in metadata_added:
                    name=new_values_dict[attribute]["attributeName"]
                    added.append(f"metadata-{attribute}-{name}")
                for key in old_values_dict:
                    if key in new_values_dict:
                        if old_values_dict[key]["attributeValue"]!=new_values_dict[key]["attributeValue"]:
                            name=old_values_dict[key]["attributeName"]
                            changed.append((f"metadata-{key}-{name}",old_values_dict[key]["attributeValue"],new_values_dict[key]["attributeValue"]))    
            elif orginal[key]!=new[key]:
                if isinstance(orginal[key],list) and isinstance(new[key],list):
                    list_removed=list(set(orginal[key])-set(new[key]))
                    list_added=list(set(new[key])-set(orginal[key]))
                    changed.append((key,tuple(list_removed),tuple(list_added)))   
                else:
                    changed.append((key,orginal[key],new[key]))    

    return json.loads(Diff(added=added,removed=removed,changed=changed).json())
def add_asset_to_db(db:ConnectionPool,data:dict,asset_id=None):
    asset=model_creator(model=Asset,err_msg="Failed to create asset from the data provided",**data)
    db_asset = asset.dict()
    check_asset_dependencies(db=db,version_id=asset.version_id,assets=asset.asset_ids)
    check_asset_metatadata(db=db,version_id=asset.version_id,metadata=asset.metadata)
    if asset_id is None:
        asset_id =services.add_asset_to_db(db=db,**db_asset)["asset_id"]
    else:
        services.update_asset(db=db,asset_id=asset_id,**db_asset)
    services.add_asset_tags_to_db(db=db,asset_id=asset_id,tags=asset.tag_ids)
    services.add_asset_projects_to_db(db=db,asset_id=asset_id,projects=asset.project_ids)
    services.add_asset_assets_to_db(db=db,asset_id=asset_id,assets=asset.asset_ids)
    services.add_asset_metadata_to_db(db=db,asset_id=asset_id,metadata=asset.metadata)
    return asset_id