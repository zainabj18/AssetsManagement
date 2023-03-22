import pytest
import json
from app.db import Models

def check_db_references(db_conn,asset_id):
    with db_conn.cursor() as cur:
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
            """SELECT * FROM audit_logs WHERE object_id=%(asset_id)s AND model_id=%(model_id)s;""",{"asset_id":asset_id,"model_id":int(Models.ASSETS)})
        assert len(cur.fetchall())==1

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
    check_db_references(db_conn=db_conn,asset_id=asset_id)

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
        data["asset_ids"]=[first_asset_id]
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
        check_db_references(db_conn=db_conn,asset_id=asset_ids[x-1])
    res = valid_client.delete(f"/api/v1/asset/{first_asset_id}")
    assert res.status_code == 200
    check_db_references(db_conn=db_conn,asset_id=first_asset_id)

