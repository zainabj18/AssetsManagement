import json
import pytest
from app.db import DataAccess, UserRole
from datetime import datetime

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
    assert datetime.fromisoformat(saved_asset["created_at"])<datetime.now()
    assert datetime.fromisoformat(saved_asset["last_modified_at"])<datetime.now()
    assert len(new_assets[0].tag_ids)==len(saved_asset['tags'])
    for tag in saved_asset['tags']:
        assert tag["id"] in new_assets[0].tag_ids
    assert len(saved_asset['metadata'])==len(data["metadata"])
    for attribute in saved_asset['metadata']:
        assert attribute in data["metadata"]
    

def test_new_assets_get_invalid_id(valid_client):
    res = valid_client.get(f"/api/v1/asset/{1}")
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
    res = valid_client.get(f"/api/v1/asset/{asset_id}")
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100}],
    indirect=True,
)
def test_new_assets_get_summary(valid_client, new_assets):
    added_assets=[]
    for asset in new_assets:
        data = json.loads(asset.json(by_alias=True))
        res = valid_client.post("/api/v1/asset/", json=data)
        assert res.status_code == 201
        assert res.json["msg"] == "Added asset"
        asset_id = res.json["data"]
        data["asset_id"]=asset_id
        added_assets.append(data)
    res = valid_client.get("/api/v1/asset/summary")
    assert res.status_code == 200
    saved_assets = res.json["data"]
    assert len(saved_assets)==len(added_assets)
    for index,saved_asset in enumerate(saved_assets):
        assert saved_asset["name"] == added_assets[index]["name"]
        assert saved_asset["link"] == str(added_assets[index]["link"])
        assert saved_asset["description"] == str(added_assets[index]["description"])
        assert saved_asset["classification"] == str(added_assets[index]["classification"])
        assert saved_asset["version_id"] ==added_assets[index]["version_id"]
        assert datetime.fromisoformat(saved_asset["created_at"])<datetime.now()
        assert datetime.fromisoformat(saved_asset["last_modified_at"])<datetime.now()

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100}],
    indirect=True,
)
def test_new_assets_get_summary_my(valid_client, new_assets):
    added_assets=[]
    for asset in new_assets:
        data = json.loads(asset.json(by_alias=True))
        res = valid_client.post("/api/v1/asset/", json=data)
        assert res.status_code == 201
        assert res.json["msg"] == "Added asset"
        asset_id = res.json["data"]
        data["asset_id"]=asset_id
        added_assets.append(data)
    res = valid_client.get("/api/v1/asset/my")
    assert res.status_code == 200
    saved_assets = res.json["data"]
    assert len(saved_assets)==len(added_assets)
    for index,saved_asset in enumerate(saved_assets):
        assert saved_asset["name"] == added_assets[index]["name"]
        assert saved_asset["link"] == str(added_assets[index]["link"])
        assert saved_asset["description"] == str(added_assets[index]["description"])
        assert saved_asset["classification"] == str(added_assets[index]["classification"])
        assert saved_asset["version_id"] ==added_assets[index]["version_id"]
        assert datetime.fromisoformat(saved_asset["created_at"])<datetime.now()
        assert datetime.fromisoformat(saved_asset["last_modified_at"])<datetime.now()


def test_new_assets_get_summary_no_assets(valid_client):
    res = valid_client.get("/api/v1/asset/summary")
    assert res.status_code == 200
    saved_assets = res.json["data"]
    assert saved_assets==[]


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC})
    ],
    indirect=True,
)  
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100}],
    indirect=True,
)
def test_new_assets_get_summary_account_privileges_check(valid_client, new_assets):
    for asset in new_assets:
        asset.classification=DataAccess.CONFIDENTIAL
        data = json.loads(asset.json(by_alias=True))
        res = valid_client.post("/api/v1/asset/", json=data)
        assert res.status_code == 201
        assert res.json["msg"] == "Added asset"
    res = valid_client.get("/api/v1/asset/summary")
    assert res.status_code == 200
    saved_assets = res.json["data"]
    assert saved_assets==[]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100}],
    indirect=True,
)
def test_assets_projects(valid_client, new_assets,db_conn):
    with db_conn.cursor() as cur:
        cur.execute("SELECT COUNT(projects) FROM projects;")
        project_count=cur.fetchone()[0]
    for asset in new_assets:
        data = json.loads(asset.json(by_alias=True))
        res = valid_client.post("/api/v1/asset/", json=data)
        assert res.status_code == 201
        assert res.json["msg"] == "Added asset"
        assert res.json["data"]
        asset_id=res.json["data"]
        res = valid_client.get(f"/api/v1/asset/projects/{asset_id}")
        assert res.status_code == 200
        asset_projects=set(data["projectIDs"])
        assert len(res.json["data"])==project_count
        for project in res.json["data"]:
            if project["isSelected"]:
                asset_projects.remove(project["projectID"])
        assert len(asset_projects)==0


def test_assets_projects_invalid_id(valid_client):
    res = valid_client.get(f"/api/v1/asset/projects/{1}")
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
def test_assets_projects_account_privileges_check(valid_client, new_assets):
    new_assets[0].classification=DataAccess.CONFIDENTIAL
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/projects/{asset_id}")
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 51}],
    indirect=True,
)
def test_assets_links(valid_client, new_assets):
    added_asset_ids=[]
    for x in range(50):
        data = json.loads(new_assets[x].json(by_alias=True))
        res = valid_client.post("/api/v1/asset/", json=data)
        assert res.status_code == 201
        assert res.json["msg"] == "Added asset"
        assert res.json["data"]
        asset_id=res.json["data"]
        added_asset_ids.append(asset_id)
    data = json.loads(new_assets[50].json(by_alias=True))
    data["assetIDs"]=added_asset_ids
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    res = valid_client.get(f"/api/v1/asset/links/{asset_id}", json=data)
    assert res.status_code == 200
    assert len(res.json["data"])==50
    for asset in res.json["data"]:
        if asset["isSelected"]:
            added_asset_ids.remove(asset["assetID"])
    assert len(added_asset_ids)==0

def test_assets_links_invalid_id(valid_client):
    res = valid_client.get(f"/api/v1/asset/links/{1}")
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
def test_assets_projects_account_privileges_check(valid_client, new_assets):
    new_assets[0].classification=DataAccess.CONFIDENTIAL
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/links/{asset_id}")
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC})
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100}],
    indirect=True,
)
def test_assets_links_with_different_classifications(valid_client, new_assets):
    added_asset_ids=[]
    for x in range(99):
        data = json.loads(new_assets[x].json(by_alias=True))
        res = valid_client.post("/api/v1/asset/", json=data)
        assert res.status_code == 201
        assert res.json["msg"] == "Added asset"
        assert res.json["data"]
        asset_id=res.json["data"]
        if new_assets[x].classification==DataAccess.PUBLIC:
            added_asset_ids.append(asset_id)
    new_assets[99].classification=DataAccess.PUBLIC
    new_assets[99].asset_ids=added_asset_ids
    data = json.loads(new_assets[99].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    res = valid_client.get(f"/api/v1/asset/links/{asset_id}", json=data)
    assert res.status_code == 200
    assert len(res.json["data"])==len(added_asset_ids)
    for asset in res.json["data"]:
        if asset["isSelected"]:
            added_asset_ids.remove(asset["assetID"])
    assert len(added_asset_ids)==0
