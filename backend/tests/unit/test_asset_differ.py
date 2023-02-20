
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
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_add_multiple_to_new(new_assets):
    old_asset=json.loads(new_assets[0].json())
    new_asset=old_asset.copy()
    new_asset["new1"]=1
    new_asset["new2"]=2
    new_asset["new3"]=3
    res=asset_differ(old_asset,new_asset)
    assert set(res["added"])==set([("new1",1),("new2",2),("new3",3)])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_to_new_str(new_assets):
    old_asset=json.loads(new_assets[0].json())
    new_asset=old_asset.copy()
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
    new_asset=old_asset.copy()
    new_asset["num"]=2
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("num",old_asset["num"],new_asset["num"])])

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":False}],
    indirect=True,
)
def test_change_multiple(new_assets):
    old_asset=json.loads(new_assets[0].json())
    old_asset["num"]=1
    old_asset["link"]="http://www.price-griffi.com/"
    new_asset=old_asset.copy()
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
    new_asset=old_asset.copy()
    new_asset["tags"]=[1, 5, 2, 7, 8, 10]
    res=asset_differ(old_asset,new_asset)
    assert set(res["changed"])==set([("tags",tuple([]),tuple([10]))])