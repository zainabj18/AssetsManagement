import pytest
from psycopg.rows import dict_row
import json
from app.db import DataAccess, UserRole
from app.schemas import Attribute


def test_new_assset_requires_name(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["name"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_link(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["link"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_type(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["type"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_description(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["description"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_tag(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["tags"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_tag(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["tags"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_classification(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["classification"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_metadata(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["metadata"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


@pytest.mark.parametrize(
    "attribute,json",
    [
        ("name", {"name": "assetName"}),
        ("link", {"link": "assetLink"}),
        ("type", {"type": "assetType"}),
        ("description", {"description": "assetDescription"}),
        ("tags", {"tags": ["assetTag1", "assetTag2"]}),
        ("access_level", {"access_level": "CONFIDENTIAL"}),
        ("project", {"project": "projectName"}),
        (
            "metadata",
            {
                "metadata": [
                    {
                        "attributeName": "programming Language(s)",
                        "attributeType": "text",
                        "attributeValue": "React,JS,CSS",
                    },
                    {
                        "attribute_name": "public",
                        "attribute_type": "checkbox",
                        "attribute_value": True,
                    },
                    {
                        "attributeName": "no. of issues",
                        "attributeType": "number",
                        "attributeValue": 2,
                    },
                ]
            },
        ),
    ],
)
def test_new_assset_tyes_correct(client, attribute, json):
    res = client.post("/api/v1/asset/", json=json)
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": [attribute],
        "msg": "field required",
        "type": "value_error.missing",
    } not in res.json["data"]


@pytest.mark.parametrize(
    "attribute,json",
    [
        ("name", {"name": []}),
        ("link", {"link": []}),
        ("type", {"type": []}),
        ("description", {"description": []})
    ],
)
def test_new_assset_string_types_incorect(client, attribute, json):
    res = client.post("/api/v1/asset/", json=json)
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": [attribute],
        "msg": "str type expected",
        "type": "type_error.str",
    } in res.json["data"]


def test_new_assset_tags_list_incorect(client):
    res = client.post("/api/v1/asset/", json={"tags": ["1", []]})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["tags", 1],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    } in res.json["data"]

def test_new_assset_project_list_incorect(client):
    res = client.post("/api/v1/asset/", json={"projects": ["1", []]})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["projects", 1],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    } in res.json["data"]

def test_new_assset_metadata_incorrect_integer(client):
    res = client.post("/api/v1/asset/", json={"metadata": 1})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["metadata"],
        "msg": "value is not a valid list",
        "type": "type_error.list",
    } in res.json["data"]
def test_new_assset_metadata_incorrect_mixed_type(client):
    res = client.post(
        "/api/v1/asset/",
        json={"metadata": [{"s": "s"}, {"attributeName": "s", "attribute_type": []}]},
    )
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["metadata", 0, "attributeName"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]
    # assert {
    #     "loc": ["metadata", 0, "attributeType"],
    #     "msg": "field required",
    #     "type": "value_error.missing",
    # } in res.json["data"]
    # assert {
    #     "loc": ["metadata", 0, "attributeValue"],
    #     "msg": "field required",
    #     "type": "value_error.missing",
    # } in res.json["data"]
    # assert {
    #     "loc": ["metadata", 1, "attributeValue"],
    #     "msg": "field required",
    #     "type": "value_error.missing",
    # } in res.json["data"]
    # assert {
    #     "loc": ["metadata", 1, "attributeType"],
    #     "msg": "str type expected",
    #     "type": "type_error.str",
    # } in res.json["data"]


def test_new_assset_requires_project(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["projects"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_incorrect_classification(client):
    res = client.post("/api/v1/asset/", json={"classification":[]})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert res.json["data"]==None

def test_get_access_levels(valid_client):
    res = valid_client.get("/api/v1/asset/classifications")
    assert res.status_code == 200
    assert res.json["data"] == ["PUBLIC", "INTERNAL", "RESTRICTED", "CONFIDENTIAL"]


def test_new_asset_tags(client,new_asset,db_conn):
    data = json.loads(new_asset.json())
    res = client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"]=="Added asset"
    assert res.json["data"]
    with db_conn.cursor() as cur:
        cur.execute("""SELECT tag_id FROM assets_in_tags WHERE asset_id=%(id)s;""", {"id": res.json["data"]})
        assert set(cur.fetchall()[0])==set(new_asset.tags)

def test_new_asset_projects(client,new_asset,db_conn):
    data = json.loads(new_asset.json())
    res = client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"]=="Added asset"
    assert res.json["data"]
    with db_conn.cursor() as cur:
        cur.execute("""SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s;""", {"id": res.json["data"]})
        assert set(cur.fetchall()[0])==set(new_asset.projects)

def test_new_asset_in_db(client,new_asset,db_conn):
    data = json.loads(new_asset.json())
    res = client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"]=="Added asset"
    assert res.json["data"]
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""SELECT * FROM assets WHERE asset_id=%(id)s;""", {"id": res.json["data"]})
        asset=cur.fetchone()
        assert asset["name"] == new_asset.name
        assert asset["link"] == new_asset.link
        assert asset["type"] == new_asset.type
        assert asset["description"] == new_asset.description
        assert asset["classification"] == new_asset.classification

def test_new_asset_values(client,new_asset,db_conn):
    data = json.loads(new_asset.json())
    res = client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"]=="Added asset"
    assert res.json["data"]
    with db_conn.cursor() as cur:
        cur.execute("""SELECT attribute_id as attribute_value FROM attributes_values WHERE asset_id=%(id)s;""", {"id": res.json["data"]})
        values=[x[0]for x in cur.fetchall()]
        for atr in new_asset.metadata:
            assert atr.attribute_id in values


def test_new_asset_get(client,new_asset):
    data = json.loads(new_asset.json())
    res = client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"]=="Added asset"
    asset_id=res.json["data"]
    res = client.get(f"/api/v1/asset/{asset_id}", json=data)
    assert res.json['data']==  json.loads(new_asset.json(by_alias=True))
    
# TODO:Test asset name is unique
# TODO:Test DB error
