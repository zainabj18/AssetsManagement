import pytest

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_tags_AND(valid_client, new_assets):
    filter_tags=new_assets[0].tags
    asset_ids=[]
    for asset in new_assets:
        if set(asset.tags).issuperset(set(filter_tags)):
            asset_ids.append(asset.asset_id)
    res = valid_client.post("/api/v1/asset/filter", json={"tags":filter_tags,"tag_operation":"AND"})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_tags_OR(valid_client, new_assets):
    filter_tags=new_assets[0].tags
    asset_ids=[]
    for asset in new_assets:
        if len(set(asset.tags).intersection(set(filter_tags)))>0:
            asset_ids.append(asset.asset_id)
    res = valid_client.post("/api/v1/asset/filter", json={"tags":filter_tags,"tag_operation":"OR"})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_projects_AND(valid_client, new_assets):
    filter_project=new_assets[0].projects
    asset_ids=[]
    for asset in new_assets:
        if set(asset.projects).issuperset(set(filter_project)):
            asset_ids.append(asset.asset_id)
    res = valid_client.post("/api/v1/asset/filter", json={"projects":filter_project,"project_operation":"AND"})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_projects_OR(valid_client, new_assets):
    filter_project=new_assets[0].projects
    asset_ids=[]
    for asset in new_assets:
        if len(set(asset.projects).intersection(set(filter_project)))>0:
            asset_ids.append(asset.asset_id)
    res = valid_client.post("/api/v1/asset/filter", json={"projects":filter_project,"project_operation":"OR"})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)


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
def test_assets_AND_missing_filters(valid_client, new_assets):
    filter_type=[new_assets[0].version_id,new_assets[1].version_id,new_assets[2].version_id]
    filter_classification=["PUBLIC","RESTRICTED"]
    res = valid_client.post("/api/v1/asset/filter", json={"types":filter_type,"classifications":filter_classification,"operation":"AND"})
    assert res.status_code == 200
    assert set(res.json["data"])==set()

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_AND(valid_client, new_assets):
    print(str(new_assets[0].classification.value))
    asset_ids=set()
    filter_type=[]
    projects_filter=[]
    tags_filter=[]
    filter_classification=["PUBLIC","RESTRICTED"]
    for x in range(70):
        filter_type.append(new_assets[x].version_id)
        if new_assets[x].classification.value in filter_classification:
            asset_ids.add(new_assets[x].asset_id)
            projects_filter.extend(new_assets[x].projects)
            tags_filter.extend(new_assets[x].tags)

    res = valid_client.post("/api/v1/asset/filter", json={"types":filter_type,"classifications":filter_classification,
                                                          "tags":tags_filter,
                                                          "projects":projects_filter,
                                                          "attributes":[{"attributeID":-1,"operation":"HAS"}],
                                                          "operation":"AND"})
    assert res.status_code == 200
    assert set(res.json["data"])==set(asset_ids)

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_OR(valid_client, new_assets):
    print(str(new_assets[0].classification.value))
    asset_ids=set()
    filter_type=[]
    projects_filter=[]
    tags_filter=[]
    filter_classification=["PUBLIC","RESTRICTED"]
    for x in range(10):
        filter_type.append(new_assets[x].version_id)
        if new_assets[x].classification.value in filter_classification:
            asset_ids.add(new_assets[x].asset_id)
            projects_filter.extend(new_assets[x].projects)
            tags_filter.extend(new_assets[x].tags)

    res = valid_client.post("/api/v1/asset/filter", json={"types":filter_type,"classifications":filter_classification,
                                                          "tags":tags_filter,
                                                          "projects":projects_filter,
                                                          "attributes":[{"attributeID":-1,"operation":"HAS"}],
                                                          "operation":"OR"})
    print(res.json["data"])
    assert res.status_code == 200
    assert set(res.json["data"]).issuperset(set(asset_ids))
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
def test_assets_filter_attribute_multiple_or(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attribute_operation":"OR","attributes":[{"attributeID":-1,"attributeValue":new_assets[0].name,"operation":"EQUALS"},
                                                                {"attributeID":-1,"attributeValue":new_assets[0].name+"!","operation":"EQUALS"}]})
    assert res.status_code == 200
    assert res.json["data"]==[new_assets[0].asset_id]



@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_assets_filter_attribute_multiple_and(valid_client, new_assets):
    res = valid_client.post("/api/v1/asset/filter", json={"attribute_operation":"AND","attributes":[{"attributeID":-1,"attributeValue":new_assets[0].name,"operation":"EQUALS"},
                                                                {"attributeID":-1,"attributeValue":new_assets[0].name+"!","operation":"EQUALS"}]})
    assert res.status_code == 200
    assert res.json["data"]==[]


