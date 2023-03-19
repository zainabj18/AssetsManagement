import pytest
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 10,"add_to_db":True}],
    indirect=True,
)
def test_related_tags(valid_client, new_assets):
    related_tags={}
    tags=set(new_assets[0].tags)
    for asset in new_assets[1:]:
        tags_in_common = len(tags.intersection(asset.tags))
        if tags_in_common>0:
            related_tags[asset.asset_id]=tags_in_common
    res = valid_client.get(f"/api/v1/asset/related/tags/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert len(res.json["data"])==len(related_tags)
    for asset in res.json["data"]:
        assert asset["count"]==related_tags[asset["assetID"]]
        related_tags.pop(asset["assetID"])
    assert len(related_tags)==0


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 10,"add_to_db":True}],
    indirect=True,
)
def test_related_projects(valid_client, new_assets):
    related_projects={}
    projects=set(new_assets[0].projects)
    for asset in new_assets[1:]:
        projects_in_common = len(projects.intersection(asset.projects))
        print(asset.projects)
        if projects_in_common>0:
            related_projects[asset.asset_id]=projects_in_common
    res = valid_client.get(f"/api/v1/asset/related/projects/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert len(res.json["data"])==len(related_projects)
    for asset in res.json["data"]:
        assert asset["count"]==related_projects[asset["assetID"]]
        related_projects.pop(asset["assetID"])
    assert len(related_projects)==0

