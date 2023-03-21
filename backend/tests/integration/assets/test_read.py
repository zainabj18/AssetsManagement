import json

import pytest
from unittest import mock
from psycopg import Error
from app.db import DataAccess, UserRole,Models,Actions
from app.schemas import Attribute
from psycopg.rows import dict_row
from collections import defaultdict
from app.schemas.factories import AttributeFactory,CommentFactory
from datetime import datetime,timedelta

def test_get_access_levels(valid_client):
    res = valid_client.get("/api/v1/asset/classifications")
    assert res.status_code == 200
    assert res.json["data"] == ["PUBLIC", "INTERNAL", "RESTRICTED", "CONFIDENTIAL"]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_get(valid_client, new_assets):
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/{asset_id}")
    assert res.status_code == 200
    saved_asset = res.json["data"]
    assert saved_asset["name"] == new_assets[0].name
    assert saved_asset["link"] == str(new_assets[0].link)
    assert saved_asset["description"] == str(new_assets[0].description)
    assert saved_asset["classification"] == str(new_assets[0].classification.value)
    assert saved_asset["version_id"] ==new_assets[0].version_id
    assert saved_asset["assets"]==[]
    assert datetime.fromisoformat(saved_asset["created_at"])<datetime.now()
    assert datetime.fromisoformat(saved_asset["last_modified_at"])<datetime.now()
    assert len(new_assets[0].tags)==len(saved_asset['tags'])
    for tag in saved_asset['tags']:
        assert tag["id"] in new_assets[0].tags
    assert len(new_assets[0].projects)==len(saved_asset['projects'])
    for project in saved_asset['projects']:
        assert project["projectID"] in new_assets[0].projects
    assert len(saved_asset['metadata'])==len(data["metadata"])
    for attribute in saved_asset['metadata']:
        assert attribute in data["metadata"]
    

def test_new_assets_get_invalid_id(valid_client):
    res = valid_client.get(f"/api/v1/asset/{1}")
    assert res.status_code == 400
    assert res.json=={'data': ['1'], 'msg': "Asset doesn't exist"}


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC})
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_get_forbidden(valid_client, new_assets):
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/{asset_id}")
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}
# # TODO:Test asset name is unique
# # TODO:Test DB error


# @pytest
# @pytest.mark.parametrize(
#     "new_assets",
#     [{"batch_size": 1,"add_to_db":True}],
#     indirect=True,
# )
# @pytest.mark.parametrize(
#     "type_verions",
#     [{"size": 10,"add_to_db": True}],
#     indirect=True,
# )
# def test_upgrade_availiable(db_conn,valid_client,new_assets,type_verions):
#     with db_conn.cursor() as cur:
#         cur.execute("SELECT type_id FROM type_version WHERE version_id=%(version_id)s",{"version_id":new_assets[0].version_id})
#         type_id=cur.fetchone()[0]
#         cur.execute(
#             """UPDATE type_version
# SET type_id = %(type_id)s""",
#             {"type_id": type_id},
#         )
#         min_version_number=min([row.version_number for row in type_verions[0]])
#         cur.execute(
#             """UPDATE type_version
# SET version_number = %(version_number)s WHERE version_id=%(version_id)s""",
#             {"version_number":min_version_number-1,"version_id":new_assets[0].version_id},
#         )
#         cur.execute(
#             """SELECT MAX(version_id) FROM type_version;""")
#         db_conn.commit()
#         max_version_id=cur.fetchone()[0]
#         max_version_attributes_id=[]
#         max_version_attributes=[]
#         for row in type_verions[0]:
#             if row.version_id==max_version_id:
#                 for attribute in row.attributes:
#                     max_version_attributes_id.append(attribute.attribute_id)
#                     max_version_attributes.append(attribute)
#         print(max_version_attributes_id)
#         cur.execute(
#             """SELECT attribute_id FROM attributes_in_types WHERE type_version=%(type_version)s ;""",{"type_version":new_assets[0].version_id})
#         old_version_attributes_id=[row[0] for row in cur.fetchall()]
       
#         res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
#         assert res.status_code == 200
#         assert res.json["msg"] == "upgrade needed"
#         assert res.json["canUpgrade"]==True
#         assert len(res.json["data"])==3
#         new_attributes_counter=0
#         for a in max_version_attributes:
#             if a.attribute_id not in old_version_attributes_id:
#                 att=a.dict(by_alias=True,exclude={"attribute_value"}) 
#                 assert att in res.json["data"][0]
#                 new_attributes_counter+=1
#             else:
#                 old_version_attributes_id.remove(a.attribute_id)
#         assert len(res.json["data"][0])==new_attributes_counter
#         print(old_version_attributes_id)
#         cur.execute(
#             """SELECT attribute_name FROM attributes WHERE attribute_id=ANY(%(attribute_ids)s);""",{"attribute_ids":old_version_attributes_id})
#         removed_names=[row[0] for row in cur.fetchall()]

#         print(removed_names)
#         assert set(res.json["data"][1])==set(removed_names)
#         assert res.json["data"][2]==max_version_id


