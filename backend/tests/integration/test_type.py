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

# Test to see if a type can be added to the database


def test_add_type_to_db(client, db_conn):
    test_type = {
        "typeName": "framework",
        "metadata": [
            {
                "attributeName": "programming Language(s)",
                "attributeType": "text",
            }
        ]
    }
    client.post("/api/v1/type/adder/new", json=test_type["metadata"][0])
    res = client.post("/api/v1/type/new", json=test_type)
    assert res.status_code == 200

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM attributes_in_types AS at INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id INNER JOIN types AS t on at.type_id = t.type_id;"""
        )
        type = cur.fetchone()
        assert type["type_name"] == test_type["typeName"]
        assert type["attribute_name"] == test_type["metadata"][0]["attributeName"]
        assert type["attribute_data_type"] == test_type["metadata"][0]["attributeType"]