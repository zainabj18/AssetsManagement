from . import services
from psycopg_pool import ConnectionPool
from typing import List
from flask import abort

def get_key_from_results(key,results):
    return [row[key] for row in results]

def check_asset_dependencies(db:ConnectionPool,version_id:int,assets:List[int]):
    asset_versions=services.fetch_assets_versions(db=db,assets_ids=assets)
    asset_types=set(get_key_from_results("version_id",asset_versions))
    dependents=services.fetch_version_dependencies(db=db,version_id=version_id)
    if not asset_types.issuperset(set(get_key_from_results("version_id",dependents))):
        abort(400, {"msg": "Missing dependencies", "data": get_key_from_results("type_name",dependents)})

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
                    print(at)
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
                print(old_values_dict)
                print(new_values_dict)
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

    return {"added":added,"removed":removed,"changed":changed}