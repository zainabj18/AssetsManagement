
import pytest
import json
import copy
from app.asset.routes import asset_differ

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_removed_empty_on_match(new_assets):
    old_asset=json.loads(new_assets[0].json())
    new_asset=copy.deepcopy(old_asset)
    res=asset_differ(old_asset,new_asset)
    assert res["removed"]==[]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_remove_from_orginal(new_assets):
    old_asset=json.loads(new_assets[0].json())
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
    old_asset=json.loads(new_assets[0].json())
    new_asset=copy.deepcopy(old_asset)
    del new_asset["link"]
    del new_asset["name"]
    del new_asset["tags"]
    res=asset_differ(old_asset,new_asset)
    assert set(res["removed"])==set(["link","name","tags"])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_add_to_new(new_assets):
    old_asset=json.loads(new_assets[0].json())
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
    old_asset=json.loads(new_assets[0].json())
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
    old_asset=json.loads(new_assets[0].json())
    new_asset=copy.deepcopy(old_asset)
    new_asset["name"]=old_asset["name"]+"new"
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("name",old_asset["name"],new_asset["name"])])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_int(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["num"]=1
    new_asset=copy.deepcopy(old_asset)
    new_asset["num"]=2
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("num",old_asset["num"],new_asset["num"])])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_boolean(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["draft"]=False
    new_asset=copy.deepcopy(old_asset)
    new_asset["draft"]=True
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("draft",old_asset["draft"],new_asset["draft"])])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_multiple(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["num"]=1
    old_asset["link"]="http://www.price-griffi.com/"
    new_asset=copy.deepcopy(old_asset)
    new_asset["name"]=old_asset["name"]+"new"
    new_asset["num"]=2
    new_asset["link"]="http://www.price2-griffi.com/"
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("num",old_asset["num"],new_asset["num"]),("name",old_asset["name"],new_asset["name"]),("link",old_asset["link"],new_asset["link"])])


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_list_add(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["tags"]=[1, 5, 2, 7, 8]
    new_asset=copy.deepcopy(old_asset)
    new_asset["tags"]=[1, 5, 2, 7, 8, 10]
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("tags",tuple([]),tuple([10]))])


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_list_remove(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["tags"]=[1, 5, 2, 7, 8]
    new_asset=copy.deepcopy(old_asset)
    new_asset["tags"]=[1, 5, 2, 7]
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("tags",tuple([8]),tuple([]))])


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_list_multiple(new_assets):
    old_asset=json.loads(new_assets[0].json())
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
    old_asset=json.loads(new_assets[0].json())
    old_asset["metadata"]=[
        {
            "attribute_id": 1,
            "attribute_name": "TRHAGaOwPNQpKDzXQwqU",
            "attribute_type": "num_lmt",
            "attribute_value": "10",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attribute_id": 2,
            "attribute_name": "AmVVOSJvnVHhwXtDsjmy",
            "attribute_type": "datetime-local",
            "attribute_value": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attribute_id": 3,
            "attribute_name": "kgMhKzcidTxblyVLgWai",
            "attribute_type": "text",
            "attribute_value": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    new_asset=copy.deepcopy(old_asset)
    new_asset["metadata"].pop()
    res=asset_differ(old_asset,new_asset)
    assert set(res["removed"])==set(["metadata-3-kgMhKzcidTxblyVLgWai"])


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_metadata_added(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["metadata"]=[
        {
            "attribute_id": 1,
            "attribute_name": "TRHAGaOwPNQpKDzXQwqU",
            "attribute_type": "num_lmt",
            "attribute_value": "10",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attribute_id": 2,
            "attribute_name": "AmVVOSJvnVHhwXtDsjmy",
            "attribute_type": "datetime-local",
            "attribute_value": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attribute_id": 3,
            "attribute_name": "kgMhKzcidTxblyVLgWai",
            "attribute_type": "text",
            "attribute_value": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    new_asset=copy.deepcopy(old_asset)
    new_asset["metadata"].append({
            "attribute_id": 4,
            "attribute_name": "kgMhKzcidTxblyVLgWai",
            "attribute_type": "text",
            "attribute_value": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        })
    res=asset_differ(old_asset,new_asset)
    assert set(res["added"])==set(["metadata-4-kgMhKzcidTxblyVLgWai"])



@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_metadata_changed(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["metadata"]=[
        {
            "attribute_id": 1,
            "attribute_name": "TRHAGaOwPNQpKDzXQwqU",
            "attribute_type": "num_lmt",
            "attribute_value": "10",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attribute_id": 2,
            "attribute_name": "AmVVOSJvnVHhwXtDsjmy",
            "attribute_type": "datetime-local",
            "attribute_value": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attribute_id": 3,
            "attribute_name": "kgMhKzcidTxblyVLgWai",
            "attribute_type": "text",
            "attribute_value": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    new_asset=copy.deepcopy(old_asset)
    new_asset["metadata"]=[
        {
            "attribute_id": 1,
            "attribute_name": "TRHAGaOwPNQpKDzXQwqU",
            "attribute_type": "num_lmt",
            "attribute_value": "9",
            "validation": {"max": 10, "min": 4},
        },
        {
            "attribute_id": 2,
            "attribute_name": "AmVVOSJvnVHhwXtDsjmy",
            "attribute_type": "datetime-local",
            "attribute_value": "1971-09-27T19:45",
            "validation": None,
        },
        {
            "attribute_id": 3,
            "attribute_name": "kgMhKzcidTxblyVLgWai",
            "attribute_type": "text",
            "attribute_value": "text-kgMhKzcidTxblyVLgWai",
            "validation": None,
        }
    ]
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([('metadata-1-TRHAGaOwPNQpKDzXQwqU', '10', '9')])