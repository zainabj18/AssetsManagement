import json

import pytest
from unittest import mock
from psycopg import Error
from app.db import DataAccess, UserRole
from app.schemas import Attribute
from psycopg.rows import dict_row
from collections import defaultdict
from app.schemas.factories import AttributeFactory
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
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_tags(valid_client, new_assets):
    filter_tags=[1,2]
    asset_ids=[]
    for asset in new_assets:
        if set(asset.tags).issuperset(set(filter_tags)):
            asset_ids.append(asset.asset_id)
    res = valid_client.post("/api/v1/asset/filter", json={"tags":filter_tags,"tag_operation":"AND"})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_upgrade_not_availiable(valid_client,new_assets):
    res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
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
def test_upgrade_availiable(db_conn,valid_client,new_assets,type_verions):
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
       
        res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
        assert res.status_code == 200
        assert res.json["msg"] == "upgrade needed"
        assert res.json["canUpgrade"]==True
        assert len(res.json["data"])==3
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
        assert res.json["data"][2]==max_version_id
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_non_optional_attributes(valid_client, new_assets):
    required_attributes = list(filter(lambda x: x.validation_data["isOptional"]==False, new_assets[0].metadata))
    attribute_ids=[attribute.attribute_id for attribute in required_attributes]
    new_assets[0].metadata=[]
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 400
    assert res.json["msg"]=="Missing required attributes"
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["data"]== f"Must inlcude the following attrubutes with ids {list(attribute_ids)}"


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_projects(valid_client, new_assets):
    filter_project=[1,2]
    asset_ids=[]
    for asset in new_assets:
        if set(asset.projects).issuperset(set(filter_project)):
            asset_ids.append(asset.asset_id)
    res = valid_client.post("/api/v1/asset/filter", json={"projects":filter_project,"project_operation":"AND"})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100}],
    indirect=True,
)
def test_new_assets_with_required_attributes(valid_client, new_assets):
    required_attributes = list(filter(lambda x: x.validation_data["isOptional"]==False, new_assets[0].metadata))
    new_assets[0].metadata=required_attributes
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    print(res.json)
    assert res.status_code == 200
    

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_classification(valid_client, new_assets):
    filter_classification=["PUBLIC","RESTRICTED"]
    asset_ids=[]
    for asset in new_assets:
        if asset.classification.value in filter_classification:
            asset_ids.append(asset.asset_id)
    res = valid_client.post("/api/v1/asset/filter", json={"classifications":filter_classification})
    assert res.status_code == 200
    print(asset_ids)
    assert set(res.json["data"])==set(asset_ids)


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_type(valid_client, new_assets):
    filter_type=[new_assets[0].version_id,new_assets[1].version_id,new_assets[2].version_id]
    asset_ids=[new_assets[0].asset_id,new_assets[1].asset_id,new_assets[2].asset_id]
    res = valid_client.post("/api/v1/asset/filter", json={"types":filter_type})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_equals_name(valid_client, new_assets):
    
    res = valid_client.post("/api/v1/asset/filter", json={"attributes":[{"attributeID":-1,"attributeValue":new_assets[0].name,"operation":"EQUALS"}]})
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set([new_assets[0].asset_id]))

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_equals_link(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attributes":[{"attributeID":-2,"attributeValue":new_assets[0].link,"operation":"EQUALS"}]})
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set([new_assets[0].asset_id]))


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_equals_description(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attributes":[{"attributeID":-3,"attributeValue":new_assets[0].description,"operation":"EQUALS"}]})
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set([new_assets[0].asset_id]))  


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_like_name(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attributes":[{"attributeID":-1,"attributeValue":new_assets[0].name,"operation":"LIKE"}]})
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set([new_assets[0].asset_id]))  

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_like_link(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attributes":[{"attributeID":-2,"attributeValue":new_assets[0].link,"operation":"LIKE"}]})
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set([new_assets[0].asset_id]))  


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_like_description(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attributes":[{"attributeID":-3,"attributeValue":new_assets[0].description,"operation":"LIKE"}]})
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set([new_assets[0].asset_id]))  

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_has_metadata(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attributes":[{"attributeID":new_assets[0].metadata[0]["attribute_id"],"attributeValue":None,"operation":"HAS"}]})
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set([new_assets[0].asset_id]))


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_multiple(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"operation":"AND","attributes":[{"attributeID":-1,"attributeValue":new_assets[0].name,"operation":"EQUALS"},
                                                                {"attributeID":-1,"attributeValue":new_assets[0].name+"!","operation":"EQUALS"}]})
    assert res.status_code == 200
    assert res.json["data"]==[]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_with_addtional_attributes(valid_client, new_assets):
    
    attribute_ids=[attribute.attribute_id for attribute in new_assets[0].metadata]
    new_assets[0].metadata.append(AttributeFactory.build(attribute_id=max(attribute_ids)+1))
    data = json.loads(new_assets[0].json())
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 400
    assert res.json["msg"]=="Addtional attributes"
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["data"]== f"Must only inlcude the following attrubutes with ids {list(attribute_ids)}"


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_add_requires_comment(valid_client, new_assets):
    res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json={})
    assert res.status_code == 400
    assert res.json["msg"]=="Failed to add comment from the data provided"
    assert res.json["error"]=="Invalid data"
    assert {
        "loc": ["comment"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]

def test_comment_add_requires_asset_in_db(valid_client):
    res = valid_client.post(f"/api/v1/asset/comment/{1}",json={"comment":"Hello World!"})
    assert res.status_code == 400
    assert res.json["msg"]=="Asset doesn't exist"
    assert res.json["data"]==[]

def test_comment_add_requires_comment(valid_client):
    res = valid_client.post(f"/api/v1/asset/comment/{1}",json={})
    assert res.status_code == 400
    assert res.json["msg"]=="Failed to add comment from the data provided"
    assert {
        "loc": ["comment"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]

def test_comment_require_not_empty(valid_client):
    res = valid_client.post(f"/api/v1/asset/comment/{1}",json={"comment":""})
    assert res.status_code == 400
    assert res.json["msg"]=="Failed to add comment from the data provided"
    print(res.json["data"])
    assert {'ctx': {'limit_value': 1}, 'loc': ['comment'], 'msg': 'ensure this value has at least 1 characters', 'type': 'value_error.any_str.min_length'} in res.json["data"]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_add_to_db(db_conn,valid_client, new_assets):
    comment="Hello World!"
    res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json={"comment":comment})
    assert res.status_code == 200
    assert res.json["msg"]=="Comment added"
    with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
            SELECT * FROM comments WHERE asset_id=%(id)s""",
                {"id":new_assets[0].asset_id}
            )
            added_comment=cur.fetchone()
            assert added_comment["account_id"]==1
            assert added_comment["asset_id"]==new_assets[0].asset_id
            assert added_comment["comment"]==comment
            assert added_comment["datetime"]<datetime.utcnow()
            assert added_comment["datetime"]>(datetime.utcnow()-timedelta(minutes=2))

# @pytest.mark.parametrize(
#     "new_assets",
#     [{"batch_size": 1,"add_to_db":True}],
#     indirect=True,
# )
# def test_comment_db_error(valid_client,new_assets):
#     comment="Hello World!"
   
#     with mock.patch(
#         "app.asset.routes.insert_comment_to_db", side_effect=Error("Fake error executing query")
#     ) as p:
#         res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json={"comment":comment})
#         assert res.status_code == 500
#         p.assert_called()
#         assert res.json == {
#             "data": ["Fake error executing query"],
#             "msg": "Database Error"
#        }
