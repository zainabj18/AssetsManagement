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
def test_new_assset_requires_name(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["name"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_link(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["link"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_version_id(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["version_id"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_description(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["description"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_tag(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["tags"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_tag(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["tags"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_classification(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["classification"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_metadata(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
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
                        "attribute_data_type": "checkbox",
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
def test_new_assset_tyes_correct(valid_client, attribute, json):
    res = valid_client.post("/api/v1/asset/", json=json)
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
        ("description", {"description": []}),
    ],
)
def test_new_assset_string_types_incorect(valid_client, attribute, json):
    res = valid_client.post("/api/v1/asset/", json=json)
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": [attribute],
        "msg": "str type expected",
        "type": "type_error.str",
    } in res.json["data"]


def test_new_assset_tags_list_incorect(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"tags": ["1", []]})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["tags", 1],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    } in res.json["data"]


def test_new_assset_project_list_incorect(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"projects": ["1", []]})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["projects", 1],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    } in res.json["data"]


def test_new_assset_metadata_incorrect_integer(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"metadata": 1})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["metadata"],
        "msg": "value is not a valid list",
        "type": "type_error.list",
    } in res.json["data"]


def test_new_assset_metadata_incorrect_mixed_type(valid_client):
    res = valid_client.post(
        "/api/v1/asset/",
        json={"metadata": [{"s": "s"}, {"attributeName": "s", "attribute_data_type": []}]},
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


def test_new_assset_requires_project(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["projects"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_incorrect_classification(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"classification": []})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert res.json["data"] == None


def test_get_access_levels(valid_client):
    res = valid_client.get("/api/v1/asset/classifications")
    assert res.status_code == 200
    assert res.json["data"] == ["PUBLIC", "INTERNAL", "RESTRICTED", "CONFIDENTIAL"]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_tags(valid_client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    with db_conn.cursor() as cur:
        cur.execute(
            """SELECT tag_id FROM assets_in_tags WHERE asset_id=%(id)s;""",
            {"id": res.json["data"]},
        )
        tags = [t[0] for t in cur.fetchall()]
        assert set(tags) == set(new_assets[0].tags)


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_projects(valid_client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    with db_conn.cursor() as cur:
        cur.execute(
            """SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s;""",
            {"id": res.json["data"]},
        )
        projects = [t[0] for t in cur.fetchall()]
        assert set(projects) == set(new_assets[0].projects)


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_in_db(valid_client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM assets WHERE asset_id=%(id)s;""", {"id": res.json["data"]}
        )
        asset = cur.fetchone()
        assert asset["name"] == new_assets[0].name
        assert asset["link"] == new_assets[0].link
        assert asset["version_id"] == new_assets[0].version_id
        assert asset["description"] == new_assets[0].description
        assert asset["classification"] == new_assets[0].classification


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_values(valid_client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    with db_conn.cursor() as cur:
        cur.execute(
            """SELECT attribute_id as attribute_value FROM attributes_values WHERE asset_id=%(id)s;""",
            {"id": res.json["data"]},
        )
        values = [x[0] for x in cur.fetchall()]
        for atr in new_assets[0].metadata:
            assert atr.attribute_id in values


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_get(valid_client, new_assets):
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/{asset_id}", json=data)
    assert res.status_code == 200
    saved_asset = res.json["data"]
    assert saved_asset["name"] == new_assets[0].name
    assert saved_asset["description"] == str(new_assets[0].description)
    assert saved_asset["classification"] == str(new_assets[0].classification.value)
    assert saved_asset["link"] == str(new_assets[0].link)


# TODO:Test asset name is unique
# TODO:Test DB error

