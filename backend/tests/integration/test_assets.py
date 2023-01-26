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