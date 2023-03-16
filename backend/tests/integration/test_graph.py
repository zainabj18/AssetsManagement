# Tests that all assets are reutrned along with the assets they link to
def test_allAssets(client, db_conn):
    create_type_query = """
    INSERT INTO types(type_name)
    VALUES('testType');
    """
    create_type_version_query = """
    INSERT INTO type_version(version_number, type_id)
    VALUES(1, 1);
    """
    create_asset_query = """
    INSERT INTO assets(name, link, version_id, description)
    VALUES(%(name)s, 'example.com', 1, 'I am a description');
    """
    link_assets_query = """
    INSERT INTO assets_in_assets(from_asset_id, to_asset_id)
    VALUES(%(from)s, %(to)s);
    """
    with db_conn as conn:
        conn.execute(create_type_query)
        conn.execute(create_type_version_query)
        for i in range(0, 5):
            string = "asset" + str(i+1)
            conn.execute(create_asset_query, {"name": string})
        conn.execute(link_assets_query, {"from": 1, "to": 2})
        conn.execute(link_assets_query, {"from": 1, "to": 3})
        conn.execute(link_assets_query, {"from": 2, "to": 1})
        conn.execute(link_assets_query, {"from": 2, "to": 4})
        conn.execute(link_assets_query, {"from": 3, "to": 2})
        conn.execute(link_assets_query, {"from": 3, "to": 4})
        conn.execute(link_assets_query, {"from": 3, "to": 5})
        conn.execute(link_assets_query, {"from": 4, "to": 1})
        conn.execute(link_assets_query, {"from": 4, "to": 5})
        conn.execute(link_assets_query, {"from": 5, "to": 1})
    res = client.get("/api/v1/graph/assets")
    assert res.status_code == 200
    data = res.json["data"]
    assert data["points"] == [
        {'id': 1, 'name': 'asset1'},
        {'id': 2, 'name': 'asset2'},
        {'id': 3, 'name': 'asset3'},
        {'id': 4, 'name': 'asset4'},
        {'id': 5, 'name': 'asset5'}
    ]
    assert data["joins"] == [
        {'from': 1, 'to': [2, 3]},
        {'from': 2, 'to': [1, 4]},
        {'from': 3, 'to': [2, 4, 5]},
        {'from': 4, 'to': [1, 5]},
        {'from': 5, 'to': [1]}
    ]
