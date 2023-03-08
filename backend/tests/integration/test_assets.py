import json

import pytest
from app.db import DataAccess, UserRole
from app.schemas import Attribute
from psycopg.rows import dict_row
from collections import defaultdict


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


def test_new_assset_requires_version_id(client):
    res = client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["error"] == "Failed to create asset from the data provided"
    assert res.json["msg"] == "Data provided is invalid"
    assert {
        "loc": ["version_id"],
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
        ("description", {"description": []}),
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
    res = client.post("/api/v1/asset/", json={"classification": []})
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
def test_new_assets_tags(client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = client.post("/api/v1/asset/", json=data)
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
def test_new_assets_projects(client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = client.post("/api/v1/asset/", json=data)
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
def test_new_assets_in_db(client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = client.post("/api/v1/asset/", json=data)
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
def test_new_assets_values(client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = client.post("/api/v1/asset/", json=data)
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


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100}],
    indirect=True,
)
def test_assets_with_tags(valid_client, new_assets):
    tags = defaultdict(list)
    for asset in new_assets:
        data = json.loads(asset.json())
        res = valid_client.post("/api/v1/asset/", json=data)
        if res.status_code == 200:
            asset_id = res.json["data"]
            for tag in asset.tags:
                tags[tag].append(asset_id)
    for tag in tags:
        res = valid_client.get(f"/api/v1/asset/tags/summary/{tag}")
        assert res.status_code == 200
        assert len(res.json["data"]["assets"]) == len(tags[tag])
        assert set(asset["asset_id"] for asset in res.json["data"]["assets"]) == set(tags[tag])


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_upgrade_not_availiable(client,new_assets):
    res = client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert res.json["msg"] == "no upgrade needed"
    assert res.json["data"] == []
    assert res.json["canUpgrade"]==False

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
def test_upgrade_availiable(db_conn,client,new_assets,type_verions):
    with db_conn.cursor() as cur:
        cur.execute("SELECT type_id FROM type_version WHERE version_id=%(version_id)s",{"version_id":new_assets[0].version_id})
        type_id=cur.fetchone()[0]
        cur.execute(
            """UPDATE type_version
SET type_id = %(type_id)s""",
            {"type_id": type_id},
        )
        min_version_number=min([row.version_number for row in type_verions[0]])
        cur.execute(
            """UPDATE type_version
SET version_number = %(version_number)s WHERE version_id=%(version_id)s""",
            {"version_number":min_version_number-1,"version_id":new_assets[0].version_id},
        )
        cur.execute(
            """SELECT MAX(version_id) FROM type_version;""")
        db_conn.commit()
        max_version_id=cur.fetchone()[0]
        max_version_attributes_id=[]
        max_version_attributes=[]
        for row in type_verions[0]:
            if row.version_id==max_version_id:
                for attribute in row.attributes:
                    max_version_attributes_id.append(attribute.attribute_id)
                    max_version_attributes.append(attribute)
        print(max_version_attributes_id)
        cur.execute(
            """SELECT attribute_id FROM attributes_in_types WHERE type_version=%(type_version)s ;""",{"type_version":new_assets[0].version_id})
        old_version_attributes_id=[row[0] for row in cur.fetchall()]
       
        res = client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
        assert res.status_code == 200
        assert res.json["msg"] == "upgrade needed"
        assert res.json["canUpgrade"]==True
        assert len(res.json["data"])==2
        new_attributes_counter=0
        for a in max_version_attributes:
            if a.attribute_id not in old_version_attributes_id:
                att=a.dict(by_alias=True,exclude={"attribute_value"}) 
                assert att in res.json["data"][0]
                new_attributes_counter+=1
            else:
                old_version_attributes_id.remove(a.attribute_id)
        assert len(res.json["data"][0])==new_attributes_counter
        print(old_version_attributes_id)
        cur.execute(
            """SELECT attribute_name FROM attributes WHERE attribute_id=ANY(%(attribute_ids)s);""",{"attribute_ids":old_version_attributes_id})
        removed_names=[row[0] for row in cur.fetchall()]

        print(removed_names)
        assert set(res.json["data"][1])==set(removed_names)