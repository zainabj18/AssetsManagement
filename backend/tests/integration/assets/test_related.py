import pytest
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 10,"add_to_db":True}],
    indirect=True,
)
def test_related_tags(valid_client, new_assets):
    related_tags={}
    tags=set(new_assets[0].tag_ids)
    for asset in new_assets[1:]:
        tags_in_common = len(tags.intersection(asset.tag_ids))
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
    projects=set(new_assets[0].project_ids)
    for asset in new_assets[1:]:
        projects_in_common = len(projects.intersection(asset.project_ids))
        print(asset.project_ids)
        if projects_in_common>0:
            related_projects[asset.asset_id]=projects_in_common
    res = valid_client.get(f"/api/v1/asset/related/projects/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert len(res.json["data"])==len(related_projects)
    for asset in res.json["data"]:
        assert asset["count"]==related_projects[asset["assetID"]]
        related_projects.pop(asset["assetID"])
    assert len(related_projects)==0


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 10,"add_to_db":True}],
    indirect=True,
)
def test_related_classification(valid_client, new_assets):
    related_classification=[]
    for asset in new_assets[1:]:
        if asset.classification==new_assets[0].classification:
            related_classification.append(asset.asset_id)
    res = valid_client.get(f"/api/v1/asset/related/classification/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert len(res.json["data"])==len(related_classification)
    for asset in res.json["data"]:
        assert asset["classification"]==new_assets[0].classification.value

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 10,"add_to_db":True}],
    indirect=True,
)
def test_related_type_version(valid_client, new_assets):
    related_versions=[]
    for asset in new_assets[1:]:
        if asset.version_id==new_assets[0].version_id:
            related_versions.append(asset.asset_id)
    res = valid_client.get(f"/api/v1/asset/related/type/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert len(res.json["data"])==len(related_versions)
    for asset in res.json["data"]:
        assert asset["version_id"]==new_assets[0].version_id


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 5,"add_to_db":True}],
    indirect=True,
)
def test_related_outgoing(db_conn,valid_client, new_assets):
    with db_conn.cursor() as cur:
        cur.execute(
            """INSERT INTO assets_in_assets(from_asset_id,to_asset_id) VALUES(%(from_id)s,%(to_id_1)s),(%(from_id)s,%(to_id_2)s);""",
            {"from_id":new_assets[0].asset_id,"to_id_1":new_assets[1].asset_id,"to_id_2":new_assets[2].asset_id}
        )
        db_conn.commit()
    assets_from=[new_assets[1].asset_id,new_assets[2].asset_id]
    res = valid_client.get(f"/api/v1/asset/related/outgoing/{new_assets[0].asset_id}")
    assert res.status_code == 200
    results=[asset["assetID"]  for asset in res.json["data"]]
    assert set(results)==set(assets_from)

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 5,"add_to_db":True}],
    indirect=True,
)
def test_related_incomming(db_conn,valid_client, new_assets):
    with db_conn.cursor() as cur:
        cur.execute(
            """INSERT INTO assets_in_assets(from_asset_id,to_asset_id) VALUES(%(from_id_1)s,%(to_id)s),(%(from_id_2)s,%(to_id)s);""",
            {"to_id":new_assets[0].asset_id,"from_id_1":new_assets[1].asset_id,"from_id_2":new_assets[2].asset_id}
        )
        db_conn.commit()
    assets=[new_assets[1].asset_id,new_assets[2].asset_id]
    res = valid_client.get(f"/api/v1/asset/related/incomming/{new_assets[0].asset_id}")
    assert res.status_code == 200
    results=[asset["assetID"]  for asset in res.json["data"]]
    assert set(results)==set(assets)