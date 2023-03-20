import json
import pytest
from psycopg.rows import dict_row
from  datetime import datetime
def test_new_assset_requires_name(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    assert {
        "loc": ["name"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_link(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["link"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_version_id(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["version_id"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_description(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["description"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_classification(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["classification"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]

def test_new_assset_requires_projects(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["projects"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_requires_tags(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["tags"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]


def test_new_assset_optional_assets(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["assets"],
        "msg": "field required",
        "type": "value_error.missing",
    } not in res.json["data"]

def test_new_assset_requires_metadata(valid_client):
    res = valid_client.post("/api/v1/asset/", json={})
    assert res.status_code == 400
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["metadata"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]

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
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": [attribute],
        "msg": "str type expected",
        "type": "type_error.str",
    } in res.json["data"]

def test_new_assset_tags_list_incorect_type(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"tags": ["1", []]})
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["tags", 1],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    } in res.json["data"]

def test_new_assset_project_list_incorect(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"projects": ["1", []]})
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["projects", 1],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    } in res.json["data"]


def test_new_assset_asssets_list_incorect(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"assets": ["1", []]})
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["assets", 1],
        "msg": "value is not a valid integer",
        "type": "type_error.integer",
    } in res.json["data"]

def test_new_assset_metadata_incorrect_integer(valid_client):
    res = valid_client.post("/api/v1/asset/", json={"metadata": 1})
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": ["metadata"],
        "msg": "value is not a valid list",
        "type": "type_error.list",
    } in res.json["data"]

@pytest.mark.parametrize(
    "attribute,json",
    [
        ("name", {"name": "assetName"}),
        ("link", {"link": "assetLink"}),
        ("type", {"type": "assetType"}),
        ("description", {"description": "assetDescription"}),
        ("tags", {"tags": ["assetTag1", "assetTag2"]}),
        ("classification", {"classification": "CONFIDENTIAL"}),
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
    assert res.json["msg"] == "Failed to create asset from the data provided"
    
    assert {
        "loc": [attribute],
        "msg": "field required",
        "type": "value_error.missing",
    } not in res.json["data"]


def test_new_assset_metadata_incorrect_mixed_type(valid_client):
    res = valid_client.post(
        "/api/v1/asset/",
        json={"metadata": [{"s": "s"}, {"attributeName": "s", "attribute_data_type": []}]},
    )
    assert res.json["msg"] == "Failed to create asset from the data provided"
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
        assert asset["created_at"]<datetime.now()
        assert asset["last_modified_at"]<datetime.now()

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_tags_in_db(valid_client, new_assets, db_conn):
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
        tags = [row[0] for row in cur.fetchall()]
        assert set(tags) == set(new_assets[0].tags)

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_projects_in_db(valid_client, new_assets, db_conn):
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    with db_conn.cursor() as cur:
        cur.execute(
            """SELECT project_id FROM assets_in_projects WHERE asset_id=%(id)s;""",
            {"id": res.json["data"]},
        )
        projects = [row[0] for row in cur.fetchall()]
        assert set(projects) == set(new_assets[0].projects)



@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_values_in_db(valid_client, new_assets, db_conn):
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
        values = [row[0] for row in cur.fetchall()]
        for atr in new_assets[0].metadata:
            assert atr.attribute_id in values
        assert len(new_assets[0].metadata)==len(values)


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_unique(valid_client, new_assets):
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 500
    assert res.json["msg"] == 'Database Error'
    assert res.json["data"]==[f'duplicate key value violates unique constraint "assets_name_key"\nDETAIL:  Key (name)=({data["name"]}) already exists.']


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 2}],
    indirect=True,
)
def test_new_assets_dependents_missing(valid_client, new_assets,db_conn):
    with db_conn.cursor() as cur:
            cur.execute(
                """
    INSERT INTO type_version_link (type_version_from, type_version_to)
    VALUES (%(from)s, %(to)s)
    """,
                {"from": new_assets[1].version_id,"to":new_assets[0].version_id},
            )
            db_conn.commit()
            cur.execute("""SELECT CONCAT(type_name,'-',version_number) AS type_name FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id WHERE version_id=%(version_id)s;""",{"version_id": new_assets[0].version_id})
            type_name=cur.fetchone()[0]
    asset_1 = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=asset_1)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    asset_2 = json.loads(new_assets[1].json())
    res = valid_client.post("/api/v1/asset/", json=asset_2)
    assert res.status_code == 400
    assert res.json["msg"] == 'Missing dependencies'
    assert res.json["data"] == [type_name]
    


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 2}],
    indirect=True,
)
def test_new_assets_dependents(valid_client, new_assets,db_conn):
    with db_conn.cursor() as cur:
            cur.execute(
                """
    INSERT INTO type_version_link (type_version_from, type_version_to)
    VALUES (%(from)s, %(to)s)
    """,
                {"from": new_assets[1].version_id,"to":new_assets[0].version_id},
            )
            db_conn.commit()
    asset_1 = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=asset_1)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    asset_id=res.json["data"]
    asset_2 = json.loads(new_assets[1].json())
    asset_2["assets"]=[asset_id]
    res = valid_client.post("/api/v1/asset/", json=asset_2)
    assert res.status_code == 200
    assert res.json["msg"] == "Added asset"
    assert res.json["data"]
    