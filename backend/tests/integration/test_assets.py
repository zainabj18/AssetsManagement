import pytest
from app.db import DataAccess
def test_new_assset_requires_name(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "name"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

def test_new_assset_requires_link(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "link"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

def test_new_assset_requires_type(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "type"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

def test_new_assset_requires_description(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "description"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

def test_new_assset_requires_tag(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "tags"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

def test_new_assset_requires_tag(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "tags"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

def test_new_assset_requires_access_level(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "access_level"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

def test_new_assset_requires_metadata(client):
    res=client.post("/api/v1/asset/new",json={})
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                "metadata"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } in res.json["data"]

@pytest.mark.parametrize("attribute,json", [("name",{"name":"assetName"}),("link",{"link":"assetLink"}),("type",{"type":"assetType"}),("description",{"description":"assetDescription"}),("tags",{"tags":["assetTag1","assetTag2"]}),("access_level",{"access_level":"CONFIDENTIAL"}),("metadata",{"metadata":[{
                "attributeName": "programming Language(s)",
                "attributeType": "text",
                "attributeValue": "React,JS,CSS"
            },
            {
                "attribute_name": "public",
                "attribute_type": "checkbox",
                "attribute_value": True
            },
            {
                "attributeName": "no. of issues",
                "attributeType": "number",
                "attributeValue": 2
            }]})])
def test_new_assset_tyes_correct(client,attribute,json):
    res=client.post("/api/v1/asset/new",json=json)
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                attribute
            ],
            "msg": "field required",
            "type": "value_error.missing"
        } not in res.json["data"]


@pytest.mark.parametrize("attribute,json", [("name",{"name":[]}),("link",{"link":[]}),("type",{"type":[]}),("description",{"description":[]})])
def test_new_assset_string_types_incorect(client,attribute,json):
    res=client.post("/api/v1/asset/new",json=json)
    assert res.status_code==400
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            "loc": [
                attribute
            ],
            "msg": 'str type expected',
            "type": 'type_error.str'
        } in res.json["data"]

def test_new_assset_tags_list_incorect(client):
    res=client.post("/api/v1/asset/new",json={"tags":["1",[]]})
    assert res.json["error"]=="Failed to create asset from the data provided"
    assert res.json["msg"]=="Data provided is invalid"
    assert  {
            'loc': ['tags', 1],
            "msg": 'str type expected',
            "type": 'type_error.str'
        } in res.json["data"]
