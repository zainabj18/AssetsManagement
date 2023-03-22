import pytest
import json
import os
from app.db import DataAccess,UserRole,Models
from psycopg.rows import dict_row
from datetime import datetime

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_upgrade_not_availiable(valid_client,new_assets):
    res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert res.json["msg"] == "no upgrade needed"
    assert res.json["data"]==[]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
@pytest.mark.parametrize(
    "type_verions",
    [{"size": 10,"add_to_db": True}],
    indirect=True,
)
def test_upgrade_availiable(db_conn,valid_client,new_assets,type_verions):
    with db_conn.cursor() as cur:
        # update type_version so every verion in db corresponds to asset's type
        lastest_type_version=type_verions["added"][-1]
        cur.execute(
            """UPDATE type_version
SET type_id = %(type_id)s WHERE version_id=%(version_id)s""",
            {"type_id": lastest_type_version.type_id,"version_id":new_assets[0].version_id}
        )
        cur.execute(
                """
    INSERT INTO type_version_link (type_version_from, type_version_to)
    VALUES (%(from)s, %(to)s)
    """,
                {"from": lastest_type_version.version_id,"to":new_assets[0].version_id},
            )
        db_conn.commit()
        res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
        assert res.status_code == 200
        assert res.json["msg"] == "upgrade needed"
        # get all old attributes
        cur.execute(
            """SELECT attribute_id FROM attributes_in_types WHERE type_version=%(type_version)s ;""",{"type_version":new_assets[0].version_id})
        old_version_attributes_id=[row[0] for row in cur.fetchall()]
        new_attributes_counter=0
        # check new attribute returned 
        for a in lastest_type_version.attributes:
            if a.attribute_id not in old_version_attributes_id:
                att=a.dict(by_alias=True,exclude={"attribute_value"}) 
                assert att in res.json["data"]["addedAttributes"]
                new_attributes_counter+=1
            else:
                old_version_attributes_id.remove(a.attribute_id)
        assert len(res.json["data"]["addedAttributes"])==new_attributes_counter
        # check that old attribute returned
        cur.execute(
            """SELECT attribute_name FROM attributes WHERE attribute_id=ANY(%(attribute_ids)s);""",{"attribute_ids":old_version_attributes_id})
        removed_names=[row[0] for row in cur.fetchall()]
        assert set(res.json["data"]["removedAttributesNames"])==set(removed_names)
        # check that depencdencies updated
        cur.execute(
            """SELECT type_name FROM type_names_versions WHERE version_id=%(version_id)s;""",{"version_id":new_assets[0].version_id})
        assert set(cur.fetchone())==set(res.json["data"]["dependsOn"])
        assert len(res.json["data"]["dependsOn"])==1
        # check new version id given
        assert res.json["data"]["maxVersion"]==lastest_type_version.version_id

def test_upgrade_assets_get_invalid_id(valid_client):
    res = valid_client.get(f"/api/v1/asset/upgrade/{1}")
    assert res.status_code == 404
    assert res.json=={'msg': "Asset doesn't exist"}


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
def test_upgrade_assets_get_account_privileges_check(valid_client, new_assets):
    new_assets[0].classification=DataAccess.CONFIDENTIAL
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/upgrade/{asset_id}")
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}

def test_patch_assets_not_in_db(valid_client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.patch(f"/api/v1/asset/{1}", json=data)
    assert res.status_code == 404
    assert res.json=={'msg': "Asset doesn't exist"}

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
def test_upgrade_assets_get_account_privileges_check(valid_client, new_assets):
    new_assets[0].classification=DataAccess.CONFIDENTIAL
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    print(res.json)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_patch_assets(valid_client, new_assets):
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}

@pytest.mark.parametrize(
    "field",
    ["name","link","description"],
)
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_patch_assets_change_fields(valid_client, new_assets,db_conn,field):
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    prev_value=data[field]
    new_value=data[field]+'a'
    data[field]=new_value
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM assets WHERE asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        asset=cur.fetchone()
        assert asset[field]==new_value
        assert asset["last_modified_at"]>asset["created_at"]
        assert asset["last_modified_at"]<datetime.now()
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==[field,prev_value,new_value]
    assert res.json["data"][0]["logID"]==2
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_patch_assets_change_classification(valid_client, new_assets,db_conn):
    new_assets[0].classification=DataAccess.CONFIDENTIAL
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    data["classification"]="PUBLIC"
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM assets WHERE asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        asset=cur.fetchone()
        assert asset["classification"]==DataAccess.PUBLIC
        assert asset["last_modified_at"]>asset["created_at"]
        assert asset["last_modified_at"]<datetime.now()
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["classification","CONFIDENTIAL","PUBLIC"]
    assert res.json["data"][0]["logID"]==2
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
@pytest.mark.parametrize(
    "type_verions",
    [{"size": 1,"add_to_db": True}],
    indirect=True,
)
def test_patch_assets_change_version_id(valid_client, new_assets,db_conn,type_verions):
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    data["version_id"]=type_verions["added"][0].version_id
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.json['msg']=='Missing required attributes'
  


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_patch_assets_change_tags(valid_client, new_assets,db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    removed_tag=data["tag_ids"].pop()
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT tag_id FROM assets_in_tags WHERE assets_in_tags.asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        tags=[row["tag_id"] for row in cur.fetchall()]
        assert set(tags)==set(data["tag_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["tag_ids",[removed_tag],[]]
    assert res.json["data"][0]["logID"]==2
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]
    data["tag_ids"]==data["tag_ids"].append(removed_tag)
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT tag_id FROM assets_in_tags WHERE assets_in_tags.asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        tags=[row["tag_id"] for row in cur.fetchall()]
        assert set(tags)==set(data["tag_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["tag_ids",[],[removed_tag]]
    assert res.json["data"][0]["logID"]==3
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_patch_assets_change_projects(valid_client, new_assets,db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    removed_project=data["project_ids"].pop()
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT project_id FROM assets_in_projects WHERE assets_in_projects.asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        tags=[row["project_id"] for row in cur.fetchall()]
        assert set(tags)==set(data["project_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["project_ids",[removed_project],[]]
    assert res.json["data"][0]["logID"]==2
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]
    data["project_ids"]==data["project_ids"].append(removed_project)
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT project_id FROM assets_in_projects WHERE assets_in_projects.asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        projects=[row["project_id"] for row in cur.fetchall()]
        assert set(projects)==set(data["project_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["project_ids",[],[removed_project]]
    assert res.json["data"][0]["logID"]==3
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]



@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 2}],
    indirect=True,
)
def test_patch_assets_change_assets(valid_client, new_assets,db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]

    data = json.loads(new_assets[1].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    link_asset_id=res.json["data"]
    data["asset_ids"].append(link_asset_id)
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT to_asset_id FROM assets_in_assets WHERE assets_in_assets.from_asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        tags=[row["to_asset_id"] for row in cur.fetchall()]
        assert set(tags)==set(data["asset_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["asset_ids",[],[link_asset_id]]
    assert res.json["data"][0]["logID"]==3
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]
    data["asset_ids"]==data["asset_ids"].pop()
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT to_asset_id FROM assets_in_assets WHERE assets_in_assets.from_asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        projects=[row["to_asset_id"] for row in cur.fetchall()]
        assert set(projects)==set(data["asset_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["asset_ids",[link_asset_id],[]]
    assert res.json["data"][0]["logID"]==4
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 2}],
    indirect=True,
)
def test_patch_assets_change_assets(valid_client, new_assets,db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]

    data = json.loads(new_assets[1].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    link_asset_id=res.json["data"]
    data["asset_ids"].append(link_asset_id)
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT to_asset_id FROM assets_in_assets WHERE assets_in_assets.from_asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        tags=[row["to_asset_id"] for row in cur.fetchall()]
        assert set(tags)==set(data["asset_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["asset_ids",[],[link_asset_id]]
    assert res.json["data"][0]["logID"]==3
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]
    data["asset_ids"]==data["asset_ids"].pop()
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT to_asset_id FROM assets_in_assets WHERE assets_in_assets.from_asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        projects=[row["to_asset_id"] for row in cur.fetchall()]
        assert set(projects)==set(data["asset_ids"])
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert res.json["data"][0]["diff"]["added"]==[]
    assert res.json["data"][0]["diff"]["removed"]==[]
    assert res.json["data"][0]["diff"]["changed"][0]==["asset_ids",[link_asset_id],[]]
    assert res.json["data"][0]["logID"]==4
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]



@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 2}],
    indirect=True,
)
def test_patch_assets_change_metadata(valid_client, new_assets,db_conn,type_verions):
    orignal_attribute_ids=[a.attribute_id for a in new_assets[0].metadata]
    data = json.loads(new_assets[0].json())
    res = valid_client.post(f"/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    data["version_id"]=type_verions["added"][0].version_id
    data["metadata"]=[json.loads(a.json(by_alias=True)) for a in type_verions["added"][0].attributes]
    res = valid_client.patch(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    assert res.json=={"msg": "Updated asset"}
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT attribute_id FROM attributes_values WHERE attributes_values.asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        attributes_in_db=[row["attribute_id"] for row in cur.fetchall()]
        assert set(attributes_in_db)==set(type_verions["added"][0].attribute_ids)
    added_attributes_ids=set(type_verions["added"][0].attribute_ids)-set(orignal_attribute_ids)
    removed_attributes_ids=set(orignal_attribute_ids)-set(type_verions["added"][0].attribute_ids)
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"]==1
    assert res.json["data"][0]["action"]=="CHANGE"
    assert len(res.json["data"][0]["diff"]["added"])==len(added_attributes_ids)
    assert len(res.json["data"][0]["diff"]["removed"])==len(removed_attributes_ids)
    assert res.json["data"][0]["diff"]["changed"][0]==["version_id",new_assets[0].version_id,type_verions["added"][0].version_id]
    assert res.json["data"][0]["logID"]==2
    assert res.json["data"][0]["modelID"]==int(Models.ASSETS)
    assert res.json["data"][0]["objectID"]==asset_id
    assert res.json["data"][0]["username"]==os.environ["DEFAULT_SUPERUSER_USERNAME"]
