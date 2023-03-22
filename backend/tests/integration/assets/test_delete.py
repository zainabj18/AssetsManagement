import pytest
import json

from app.db import Models,UserRole,DataAccess,Actions
from psycopg.rows import dict_row
def check_db_references(db_conn,asset_id,valid_client):
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM assets WHERE asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        assert cur.fetchone() is None
        cur.execute(
            """SELECT * FROM assets_in_assets WHERE from_asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        assert cur.fetchone() is None
        cur.execute(
            """SELECT * FROM assets_in_assets WHERE to_asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        assert cur.fetchone() is None
        cur.execute(
            """SELECT * FROM attributes_values WHERE asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        assert cur.fetchone() is None
        cur.execute(
            """SELECT * FROM assets_in_tags WHERE asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        assert cur.fetchone() is None
        cur.execute(
            """SELECT * FROM assets_in_projects WHERE asset_id=%(asset_id)s;""",{"asset_id":asset_id})
        assert cur.fetchone() is None
        cur.execute(
            """SELECT * FROM audit_logs WHERE object_id=%(asset_id)s AND model_id=%(model_id)s ORDER BY log_id DESC;""",{"asset_id":asset_id,"model_id":int(Models.ASSETS)})
        logs=cur.fetchall()
        assert len(logs)==2
        assert logs[0]["account_id"]==1
        assert logs[0]["action"]==Actions.DELETE
        assert logs[0]["diff"]=={}
        assert logs[0]["model_id"]==int(Models.ASSETS)
        assert logs[0]["object_id"]==asset_id
        res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
        assert res.status_code == 404


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_delete(valid_client, new_assets,db_conn):
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.delete(f"/api/v1/asset/{asset_id}")
    assert res.status_code == 200
    check_db_references(db_conn=db_conn,asset_id=asset_id,valid_client=valid_client)

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 11}],
    indirect=True,
)
def test_delete_with_links(valid_client, new_assets,db_conn):
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    first_asset_id = res.json["data"]
    asset_ids=[]
    expected_dependencies=[]
    for x in range(1,10):
        data = json.loads(new_assets[x].json(by_alias=True))
        data["assetIDs"]=[first_asset_id]
        res = valid_client.post("/api/v1/asset/", json=data)
        assert res.status_code == 201
        assert res.json["msg"] == "Added asset"
        asset_id = res.json["data"]
        asset_ids.append(asset_id)
        expected_dependencies.append({"assetID":asset_id,"name":data["name"]})
    res = valid_client.delete(f"/api/v1/asset/{first_asset_id}")
    assert res.status_code == 400
    assert res.json["msg"] == "Asset has dependencies"
    assert len(res.json["data"])==len(expected_dependencies)
    for dep in res.json["data"]:
        assert dep in expected_dependencies
    # update first 5 assets to remove dependencies
    for x in range(1,5):
        data = json.loads(new_assets[x].json(by_alias=True))
        data["asset_ids"]=[]
        res = valid_client.patch(f"/api/v1/asset/{asset_ids[x-1]}", json=data)
        assert res.status_code == 200
        assert res.json["msg"] == "Updated asset"
    # delete remaining remove dependencies
    for x in range(5,10):
        data = json.loads(new_assets[x].json(by_alias=True))
        data["asset_ids"]=[]
        res = valid_client.delete(f"/api/v1/asset/{asset_ids[x-1]}")
        assert res.status_code == 200
        check_db_references(db_conn=db_conn,asset_id=asset_ids[x-1],valid_client=valid_client)
    res = valid_client.delete(f"/api/v1/asset/{first_asset_id}")
    assert res.status_code == 200
    check_db_references(db_conn=db_conn,asset_id=first_asset_id,valid_client=valid_client)



def test_delete_get_invalid_id(valid_client):
    res = valid_client.delete(f"/api/v1/asset/{1}")
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
def test_new_assets_get_account_privileges_check(valid_client, new_assets):
    new_assets[0].classification=DataAccess.CONFIDENTIAL
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.delete(f"/api/v1/asset/{asset_id}")
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}
