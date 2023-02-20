
import pytest
import json
from app.asset.routes import asset_differ

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 10,"add_to_db":False}],
    indirect=True,
)
def test_removed_empty_on_match(new_assets):
    old_asset=json.loads(new_assets[0].json())
    new_asset=old_asset.copy()
    res=asset_differ(old_asset,new_asset)
    assert res["removed"]==[]