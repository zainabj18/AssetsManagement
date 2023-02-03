import pytest
from psycopg.rows import dict_row

from app.db import DataAccess
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


def test_new_assset_requires_access_level(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["access_level"],
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
        ("description", {"description": []}),
        ("project", {"project": []}),
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
        "msg": "str type expected",
        "type": "type_error.str",
    } in res.json["data"]


def test_new_assset_acces_level_incorrect(client):
    res = client.post("/api/v1/asset/", json={"access_level": []})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert None == res.json["data"]


def test_new_assset_metadata_incorrect(client):
    res = client.post("/api/v1/asset/", json={"metadata": 1})
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["metadata"],
        "msg": "value is not a valid list",
        "type": "type_error.list",
    } in res.json["data"]

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
    assert {
        "loc": ["metadata", 0, "attributeType"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]
    assert {
        "loc": ["metadata", 0, "attributeValue"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]
    assert {
        "loc": ["metadata", 1, "attributeValue"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]
    assert {
        "loc": ["metadata", 1, "attributeType"],
        "msg": "str type expected",
        "type": "type_error.str",
    } in res.json["data"]


def test_new_assset_requires_project(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["project"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_asset_added_to_db(client, db_conn):
    data = {
        "name": "My Framework",
        "link": "https://github.com/",
        "type": "Framework",
        "description": "A custom frontend framework",
        "tags": ["React", "UI"],
        "project": "General",
        "access_level": "PUBLIC",
        "metadata": [
            {
                "attributeName": "programming Language(s)",
                "attributeType": "text",
                "attributeValue": "React,JS,CSS",
            },
            {
                "attributeName": "public",
                "attributeType": "checkbox",
                "attributeValue": True,
            },
            {
                "attributeName": "no. of issues",
                "attributeType": "number",
                "attributeValue": 2,
            },
            {
                "attributeName": "built on",
                "attributeType": "datetime-local",
                "attributeValue": "2021-12-10T13:45",
            },
            {
                "attributeName": "version",
                "attributeType": "text",
                "attributeValue": "v1",
            },
        ],
    }
    res = client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM assets WHERE name=%(name)s;""", {"name": data["name"]}
        )
        asset = cur.fetchone()
        assert asset["name"] == data["name"]
        assert asset["link"] == data["link"]
        assert asset["type"] == data["type"]
        assert asset["description"] == data["description"]
        assert asset["tags"] == data["tags"]
        assert asset["project"] == data["project"]
        assert asset["access_level"] == DataAccess.PUBLIC
        assert asset["metadata"] == [Attribute(**x) for x in data["metadata"]]


def test_get_asset_added_to_db(client):
    data = {
        "name": "My Framework",
        "link": "https://github.com/",
        "type": "Framework",
        "description": "A custom frontend framework",
        "tags": ["React", "UI"],
        "project": "General",
        "access_level": "PUBLIC",
        "metadata": [
            {
                "attributeName": "programming Language(s)",
                "attributeType": "text",
                "attributeValue": "React,JS,CSS",
            },
            {
                "attributeName": "public",
                "attributeType": "checkbox",
                "attributeValue": True,
            },
            {
                "attributeName": "no. of issues",
                "attributeType": "number",
                "attributeValue": 2,
            },
            {
                "attributeName": "built on",
                "attributeType": "datetime-local",
                "attributeValue": "2021-12-10T13:45",
            },
            {
                "attributeName": "version",
                "attributeType": "text",
                "attributeValue": "v1",
            },
        ],
    }
    res = client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    res = client.get("/api/v1/asset/1")
    assert res.status_code == 200
    asset = res.json
    assert asset["name"] == data["name"]
    assert asset["link"] == data["link"]
    assert asset["type"] == data["type"]
    assert asset["description"] == data["description"]
    assert asset["tags"] == data["tags"]
    assert asset["project"] == data["project"]
    assert asset["access_level"] == "PUBLIC"
    assert asset["metadata"] == [Attribute(**x) for x in data["metadata"]]

def test_get_access_levels(client):
    res = client.get(
        "/api/v1/asset/classifications"
    )
    assert res.status_code == 200
    assert res.json["data"]==['PUBLIC', 'INTERNAL', 'RESTRICTED', 'CONFIDENTIAL']