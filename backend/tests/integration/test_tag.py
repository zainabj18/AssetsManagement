def test_tag_create_requires_name(client):
    res = client.post("/api/v1/tag/",json={})
    assert res.status_code == 400
    assert res.json=={'data': [{'loc': ['name'],
                    'msg': 'field required',
                    'type': 'value_error.missing'}],
            'error': 'Failed to create tag from the data provided',
            'msg': 'Data provided is invalid'}
