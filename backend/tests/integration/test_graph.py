from psycopg.rows import dict_row

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
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(create_type_query)
        cur.execute(create_type_version_query)
        for i in range(0, 5):
            string = "asset" + str(i)
            cur.execute(create_asset_query, {"name": string})
    res = client.get("/api/v1/graph/assets")
    assert res.status_code == 200