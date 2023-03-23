
import pytest
import json
import copy
from app.asset.utils import asset_differ

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_removed_empty_on_match(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    new_asset=copy.deepcopy(old_asset)
    res=asset_differ(old_asset,new_asset)
    assert res["removed"]==[]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_remove_from_orginal(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    new_asset=copy.deepcopy(old_asset)
    del new_asset["link"]
    res=asset_differ(old_asset,new_asset)
    assert set(res["removed"])==set(["link"])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_remove_multiple_from_orginal(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    new_asset=copy.deepcopy(old_asset)
    del new_asset["link"]
    del new_asset["name"]
    del new_asset["tagIDs"]
    res=asset_differ(old_asset,new_asset)
    assert set(res["removed"])==set(["link","name","tagIDs"])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_add_to_new(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    new_asset=copy.deepcopy(old_asset)
    new_asset["new"]=1
    res=asset_differ(old_asset,new_asset)
    assert set(res["added"])==set(["new"])
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_add_multiple_to_new(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    new_asset=copy.deepcopy(old_asset)
    new_asset["new1"]=1
    new_asset["new2"]=2
    new_asset["new3"]=3
    res=asset_differ(old_asset,new_asset)
    assert set(res["added"])==set(["new1","new2","new3"])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_str(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    new_asset=copy.deepcopy(old_asset)
    new_asset["name"]=old_asset["name"]+"new"
    res=asset_differ(old_asset,new_asset)
    assert res["changed"]==[["name",old_asset["name"],new_asset["name"]]]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_int(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["num"]=1
    new_asset=copy.deepcopy(old_asset)
    new_asset["num"]=2
    res=asset_differ(old_asset,new_asset)
    assert res["changed"]==[["num",old_asset["num"],new_asset["num"]]]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_boolean(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["draft"]=False
    new_asset=copy.deepcopy(old_asset)
    new_asset["draft"]=True
    res=asset_differ(old_asset,new_asset)
    assert res["changed"]==[["draft",old_asset["draft"],new_asset["draft"]]]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_multiple(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["num"]=1
    old_asset["link"]="http://www.price-griffi.com/"
    new_asset=copy.deepcopy(old_asset)
    new_asset["name"]=old_asset["name"]+"new"
    new_asset["num"]=2
    new_asset["link"]="http://www.price2-griffi.com/"
    res=asset_differ(old_asset,new_asset)
    changes=[["num",old_asset["num"],new_asset["num"]],["name",old_asset["name"],new_asset["name"]],["link",old_asset["link"],new_asset["link"]]]
    for x in  changes:
        assert x in res["changed"]
    assert len(changes)==len(res["changed"])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_list_add(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["tagIDs"]=[1, 5, 2, 7, 8]
    new_asset=copy.deepcopy(old_asset)
    new_asset["tagIDs"]=[1, 5, 2, 7, 8, 10]
    res=asset_differ(old_asset,new_asset)
    assert res["changed"]==[["tagIDs",[],[10]]]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_list_remove(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["tags"]=[1, 5, 2, 7, 8]
    new_asset=copy.deepcopy(old_asset)
    new_asset["tags"]=[1, 5, 2, 7]
    res=asset_differ(old_asset,new_asset)
    assert res["changed"]==[["tags",[8],[]]]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_list_multiple(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["tags"]=[1, 5, 2, 7, 8]
    new_asset=copy.deepcopy(old_asset)
    new_asset["tags"]=[5, 2, 7,19,20]
    res=asset_differ(old_asset,new_asset)
    assert res["changed"][0][0]=="tags"
    assert set(res["changed"][0][1])==set([8,1])
    assert set(res["changed"][0][2])==set([19,20])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_metadata_removed(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["metadata"]=[
        {
            "attributeID": 1,
            "attributeName": "TRHAGaOwPNQpKDzXQwqU",
            "attributeType": "num_lmt",
            "attributeValue": "10",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attributeID": 2,
            "attributeName": "AmVVOSJvnVHhwXtDsjmy",
            "attributeType": "datetime-local",
            "attributeValue": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attributeID": 3,
            "attributeName": "kgMhKzcidTxblyVLgWai",
            "attributeType": "text",
            "attributeValue": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    new_asset=copy.deepcopy(old_asset)
    new_asset["metadata"].pop()
    res=asset_differ(old_asset,new_asset)
    assert res["removed"]==["metadata-3-kgMhKzcidTxblyVLgWai"]


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_metadata_added(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["metadata"]=[
        {
            "attributeID": 1,
            "attributeName": "TRHAGaOwPNQpKDzXQwqU",
            "attributeType": "num_lmt",
            "attributeValue": "10",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attributeID": 2,
            "attributeName": "AmVVOSJvnVHhwXtDsjmy",
            "attributeType": "datetime-local",
            "attributeValue": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attributeID": 3,
            "attributeName": "kgMhKzcidTxblyVLgWai",
            "attributeType": "text",
            "attributeValue": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    new_asset=copy.deepcopy(old_asset)
    new_asset["metadata"].append({
            "attributeID": 4,
            "attributeName": "kgMhKzcidTxblyVLgWai",
            "attributeType": "text",
            "attributeValue": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        })
    res=asset_differ(old_asset,new_asset)
    assert res["added"]==["metadata-4-kgMhKzcidTxblyVLgWai"]



@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_metadata_changed(new_assets):
    old_asset=json.loads(new_assets[0].json(by_alias=True,exclude={'created_at', 'last_modified_at'}))
    old_asset["metadata"]=[
        {
            "attributeID": 1,
            "attributeName": "TRHAGaOwPNQpKDzXQwqU",
            "attributeType": "num_lmt",
            "attributeValue": "10",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attributeID": 2,
            "attributeName": "AmVVOSJvnVHhwXtDsjmy",
            "attributeType": "datetime-local",
            "attributeValue": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attributeID": 3,
            "attributeName": "kgMhKzcidTxblyVLgWai",
            "attributeType": "text",
            "attributeValue": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    new_asset=copy.deepcopy(old_asset)
    new_asset["metadata"]=[
        {
            "attributeID": 1,
            "attributeName": "TRHAGaOwPNQpKDzXQwqU",
            "attributeType": "num_lmt",
            "attributeValue": "9",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attributeID": 2,
            "attributeName": "AmVVOSJvnVHhwXtDsjmy",
            "attributeType": "datetime-local",
            "attributeValue": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attributeID": 3,
            "attributeName": "kgMhKzcidTxblyVLgWai",
            "attributeType": "text",
            "attributeValue": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    res=asset_differ(old_asset,new_asset)
    assert res["changed"]==[['metadata-1-TRHAGaOwPNQpKDzXQwqU', '10', '9']]