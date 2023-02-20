
import pytest
import json
from app.asset.routes import asset_differ

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_removed_empty_on_match(new_assets):
    old_asset=json.loads(new_assets[0].json())
    new_asset=old_asset.copy()
    res=asset_differ(old_asset,new_asset)
    assert res["removed"]==[]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_remove_from_orginal(new_assets):
    old_asset=json.loads(new_assets[0].json())
    new_asset=old_asset.copy()
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
    new_asset=old_asset.copy()
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
    new_asset=old_asset.copy()
    new_asset["new"]=1
    res=asset_differ(old_asset,new_asset)
    assert set(res["added"])==set([("new",1)])