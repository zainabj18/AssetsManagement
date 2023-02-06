from psycopg.rows import dict_row

# Test for the path to the type adder


def test_typeAdder_route(client):
    res = client.get("/api/v1/type/adder")
    assert res.status_code == 200

# Test to see if an asset can be added to the database


def test_add_attribute_to_db(client, db_conn):
    test_attribute = {
        "attributeName": "public",
        "attributeType": "checkbox",
    }
    res = client.post("/api/v1/type/adder/new", json=test_attribute)
    assert res.status_code == 200

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM attributes WHERE attribute_name=%(name)s AND attribute_data_type=%(type)s;""",
            {"name": test_attribute["attributeName"],
                "type": test_attribute["attributeType"]}
        )
        attribute = cur.fetchone()
        assert attribute["attribute_name"] == test_attribute["attributeName"]
        assert attribute["attribute_data_type"] == test_attribute["attributeType"]
