from psycopg.rows import dict_row

# Test for the path to the type adder


def test_typeAdder_route(client):
    res = client.get("/api/v1/type/adder")
    assert res.status_code == 200

# Test to see if an attribute can be added to the database


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

# Test to see if an attribute can be added to the database with validation
def test_add_attribute_to_db_with_json(client, db_conn):
    test_attribute = {
        "attributeName": "public",
        "attributeType": "checkbox",
        "validation": {
            "min": 4,
            "max": 10
        }
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
        assert attribute["validation_data"] == test_attribute["validation"]

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

# Test to see if a type can be returned from the database


def test_get_type(client):
    test_type = {
        "typeName": "library",
        "metadata": [
            {
                "attributeName": "age",
                    "attributeType": "number",
            }
        ]
    }
    client.post("/api/v1/type/adder/new", json=test_type["metadata"][0])
    client.post("/api/v1/type/new", json=test_type)
    res = client.get("/api/v1/type/1")
    assert res.status_code == 200
    type = res.json
    assert type == test_type

# Test to see if a list of all attributes can be returned from the database


def test_get_allAttributes(client):
    test_attributes = [
        {
            "attributeName": "issues",
            "attributeType": "text",
        },
        {
            "attributeName": "public",
            "attributeType": "checkbox",
        },
        {
            "attributeName": "author",
            "attributeType": "text",
        }
    ]
    client.post("/api/v1/type/adder/new", json=test_attributes[0])
    client.post("/api/v1/type/adder/new", json=test_attributes[1])
    client.post("/api/v1/type/adder/new", json=test_attributes[2])
    res = client.get("/api/v1/type/allAttributes")
    assert res.status_code == 200
    attributes = res.json
    assert attributes == test_attributes


# Test to see if a list of all types can be returned from the database


def test_get_allTypes(client):
    test_types = [
        {
            "typeId": 1,
            "typeName": "framework",
            "metadata": [
                {
                        "attributeName": "programming Language(s)",
                        "attributeType": "text",
                }
            ]
        },
        {
            "typeId": 2,
            "typeName": "libary",
            "metadata": [
                {
                        "attributeName": "author",
                        "attributeType": "text",
                },
                {
                    "attributeName": "age",
                    "attributeType": "number",
                }
            ]
        }
    ]
    client.post("/api/v1/type/adder/new",
                json=test_types[0]["metadata"][0])
    client.post("/api/v1/type/new", json=test_types[0])
    client.post("/api/v1/type/adder/new",
                json=test_types[1]["metadata"][0])
    client.post("/api/v1/type/adder/new",
                json=test_types[1]["metadata"][1])
    client.post("/api/v1/type/new", json=test_types[1])
    res = client.get("/api/v1/type/allTypes")
    assert res.status_code == 200
    types = res.json
    assert types == test_types
