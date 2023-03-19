# Poplates db with 'count' number of assets
def populate_db_assets(db_conn, count):
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
    with db_conn as conn:
        conn.execute(create_type_query)
        conn.execute(create_type_version_query)
        for i in range(0, count):
            string = "asset" + str(i+1)
            conn.execute(create_asset_query, {"name": string})

# Tests that all assets are reutrned along with the assets they link to


def test_all_assets(client, db_conn):
    link_assets_query = """
    INSERT INTO assets_in_assets(from_asset_id, to_asset_id)
    VALUES(%(from)s, %(to)s);
    """
    populate_db_assets(db_conn, 5)
    with db_conn as conn:
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


# Gets all incomming and outgoing relations for a single asset
def test_single_asset(client, db_conn):
    link_assets_query = """
    INSERT INTO assets_in_assets(from_asset_id, to_asset_id)
    VALUES(%(from)s, %(to)s);
    """
    populate_db_assets(db_conn, 5)
    with db_conn as conn:
        conn.execute(link_assets_query, {"from": 1, "to": 2})
        conn.execute(link_assets_query, {"from": 2, "to": 3})
        conn.execute(link_assets_query, {"from": 2, "to": 5})
        conn.execute(link_assets_query, {"from": 4, "to": 2})
        conn.execute(link_assets_query, {"from": 5, "to": 2})
    res = client.get("/api/v1/graph/asset/2")
    assert res.status_code == 200