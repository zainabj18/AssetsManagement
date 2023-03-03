from psycopg.rows import dict_row


def test_type_list(client, db_conn):
    expected_types = []
    with db_conn.cursor() as cur:
        for x in range(100):
            name = f"Test-{x}"
            type = {"type_name": name}
            cur.execute(
                """
    INSERT INTO types (type_name)
VALUES (%(type_name)s) RETURNING type_id;""",
                type,
            )
            id = cur.fetchone()[0]
            type["type_id"] = id
            expected_types.append(type)
        db_conn.commit()
    res = client.get("/api/v1/type/names")
    assert res.status_code == 200
    assert res.json == {"msg": "types", "data": expected_types}


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
            {
                "name": test_attribute["attributeName"],
                "type": test_attribute["attributeType"],
            },
        )
        attribute = cur.fetchone()
        assert attribute["attribute_name"] == test_attribute["attributeName"]
        assert attribute["attribute_data_type"] == test_attribute["attributeType"]


# Test to see if an attribute can be added to the database with validation
def test_add_attribute_to_db_with_json(client, db_conn):
    test_attribute = {
        "attributeName": "public",
        "attributeType": "checkbox",
        "validation": {"min": 4, "max": 10},
    }
    res = client.post("/api/v1/type/adder/new", json=test_attribute)
    assert res.status_code == 200

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM attributes WHERE attribute_name=%(name)s AND attribute_data_type=%(type)s;""",
            {
                "name": test_attribute["attributeName"],
                "type": test_attribute["attributeType"],
            },
        )
        attribute = cur.fetchone()
        assert attribute["attribute_name"] == test_attribute["attributeName"]
        assert attribute["attribute_data_type"] == test_attribute["attributeType"]
        assert attribute["validation_data"] == test_attribute["validation"]


# Test to see if a type can be added to the database
def test_add_type_to_db(client, db_conn):
    test_metaData = {
        "attributeName": "programming Language(s)",
        "attributeType": "text"
    }
    test_type = {
        "typeName": "framework",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": test_metaData["attributeName"],
                "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": []
    }
    client.post("/api/v1/type/adder/new", json=test_metaData)
    res = client.post("/api/v1/type/new", json=test_type)
    assert res.status_code == 200

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM attributes_in_types AS at
            INNER JOIN attributes AS a ON at.attribute_id = a.attribute_id
            INNER JOIN type_version AS tv ON at.type_version = tv.version_id
            INNER JOIN types AS t ON tv.type_id = t.type_id;"""
        )
        type = cur.fetchone()
        assert type["type_name"] == test_type["typeName"]
        assert type["attribute_name"] == test_type["metadata"][0]["attributeName"]
        assert type["attribute_data_type"] == test_type["metadata"][0]["attributeType"]
        assert type["version_id"] == 1


# Test to see if dependecies can be added
def test_add_type_with_dependencies(client, db_conn):
    test_metaData = {
        "attributeName": "programming Language(s)",
        "attributeType": "text"
    }
    test_type_a = {
        "typeName": "framework",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": test_metaData["attributeName"],
                "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": []
    }
    test_type_b = {
        "typeName": "Web app",
        "metadata": [
            {
                "attributeID": 1,
                    "attributeName": test_metaData["attributeName"],
                    "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": [1]
    }
    test_type_c = {
        "typeName": "internet",
        "metadata": [
            {
                "attributeID": 1,
                    "attributeName": test_metaData["attributeName"],
                    "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": [2, 1]
    }
    client.post("/api/v1/type/adder/new", json=test_metaData)
    client.post("/api/v1/type/new", json=test_type_a)
    client.post("/api/v1/type/new", json=test_type_b)
    client.post("/api/v1/type/new", json=test_type_c)
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM type_version_link"""
        )
        res = cur.fetchall()
        assert res[0]["type_version_from"] == 2
        assert res[0]["type_version_to"] == 1
        assert res[1]["type_version_from"] == 3
        assert res[1]["type_version_to"] == 2
        assert res[2]["type_version_from"] == 3
        assert res[2]["type_version_to"] == 1


# Test to make sure that no type can depend on itself
def test_no_self_dependencies(client):
    test_metaData = {
        "attributeName": "programming Language(s)",
        "attributeType": "text"
    }
    test_type = {
        "typeName": "framework",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": test_metaData["attributeName"],
                "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": [1]
    }
    client.post("/api/v1/type/adder/new", json=test_metaData)
    res = client.post("/api/v1/type/new", json=test_type)
    assert res.status_code == 422


# Test to see if a type can be returned from the database
def test_get_type(client):
    test_type = {
        "typeId": 1,
        "typeName": "library",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": "age",
                "attributeType": "number",
                "validation": None,
            }
        ],
        "dependsOn": []
    }
    client.post("/api/v1/type/adder/new", json=test_type["metadata"][0])
    client.post("/api/v1/type/new", json=test_type)
    res = client.get("/api/v1/type/1")
    assert res.status_code == 200
    type = res.json
    assert type["typeName"] == test_type["typeName"]
    assert type["metadata"] == test_type["metadata"]


# Test to see if a type can be returned from the database
def test_get_type_with_json(client):
    test_type = {
        "typeId": 1,
        "typeName": "library",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": "age",
                "attributeType": "number",
                "validation": {"min": 4, "max": 10},
            }
        ],
        "dependsOn": []
    }
    client.post("/api/v1/type/adder/new", json=test_type["metadata"][0])
    client.post("/api/v1/type/new", json=test_type)
    res = client.get("/api/v1/type/1")
    assert res.status_code == 200
    type = res.json
    assert type["typeName"] == test_type["typeName"]
    assert type["metadata"] == test_type["metadata"]


# Test to see if a list of all attributes can be returned from the database
def test_get_allAttributes(client):
    test_attributes = [
        {
            "attributeID": 1,
            "attributeName": "issues",
            "attributeType": "text",
            "validation": None,
        },
        {
            "attributeID": 2,
            "attributeName": "public",
            "attributeType": "checkbox",
            "validation": None,
        },
        {
            "attributeID": 3,
            "attributeName": "author",
            "attributeType": "text",
            "validation": None,
        },
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
                    "attributeID": 1,
                    "attributeName": "programming Language(s)",
                    "attributeType": "text",
                    "validation": None,
                }
            ],
            "dependsOn": []
        },
        {
            "typeId": 2,
            "typeName": "libary",
            "metadata": [
                {
                    "attributeID": 2,
                    "attributeName": "author",
                    "attributeType": "text",
                    "validation": None,
                },
                {
                    "attributeID": 3,
                    "attributeName": "age",
                    "attributeType": "number",
                    "validation": None,
                },
            ],
            "dependsOn": []
        },
    ]
    client.post("/api/v1/type/adder/new", json=test_types[0]["metadata"][0])
    client.post("/api/v1/type/new", json=test_types[0])
    client.post("/api/v1/type/adder/new", json=test_types[1]["metadata"][0])
    client.post("/api/v1/type/adder/new", json=test_types[1]["metadata"][1])
    client.post("/api/v1/type/new", json=test_types[1])
    res = client.get("/api/v1/type/allTypes")
    assert res.status_code == 200
    types = res.json
    for i in range(0, len(types)):
        type = types[i]
        test_type = test_types[i]
        assert type["typeName"] == test_type["typeName"]
        assert type["metadata"] == test_type["metadata"]
        assert type["versionNumber"] == 1


# Test that a type can be deleted
def test_delete_type(client, db_conn):
    test_type = {
        "typeId": 1,
        "typeName": "library",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": "age",
                "attributeType": "number",
                "validation": {"min": 4, "max": 10},
            }
        ],
        "dependsOn": []
    }
    client.post("/api/v1/type/adder/new", json=test_type["metadata"][0])
    client.post("/api/v1/type/new", json=test_type)
    res = client.post("/api/v1/type/delete/1")
    assert res.status_code == 200
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM type_version WHERE version_id = 1"""
        )
        assert cur.fetchone() == None


# Test that a complex type can be deleted and that depended ones wont
def test_delete_complex_type(client):
    test_metaData = {
        "attributeName": "programming Language(s)",
        "attributeType": "text"
    }
    test_type_a = {
        "typeName": "framework",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": test_metaData["attributeName"],
                "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": []
    }
    test_type_b = {
        "typeName": "Web app",
        "metadata": [
            {
                "attributeID": 1,
                    "attributeName": test_metaData["attributeName"],
                    "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": [1]
    }
    client.post("/api/v1/type/adder/new", json=test_metaData)
    client.post("/api/v1/type/new", json=test_type_a)
    client.post("/api/v1/type/new", json=test_type_b)
    res = client.post("/api/v1/type/delete/1")
    assert res.data == b'{\n  "msg": "",\n  "wasAllowed": false\n}\n'
    res = client.post("/api/v1/type/delete/2")
    assert res.data == b'{\n  "msg": "",\n  "wasAllowed": true\n}\n'
    res = client.post("/api/v1/type/delete/1")
    assert res.data == b'{\n  "msg": "",\n  "wasAllowed": true\n}\n'


# Test that an attribute can be deleted
def test_delete_attribute(client):
    test_metaData = {
        "attributeName": "programming Language(s)",
        "attributeType": "text"
    }
    test_type = {
        "typeName": "framework",
        "metadata": [
            {
                "attributeID": 1,
                "attributeName": test_metaData["attributeName"],
                "attributeType": test_metaData["attributeType"]
            }
        ],
        "dependsOn": []
    }
    client.post("/api/v1/type/adder/new", json=test_metaData)
    client.post("/api/v1/type/new", json=test_type)
    res = client.post("/api/v1/type/attribute/delete/1")
    assert res.data == b'{\n  "msg": "",\n  "wasAllowed": false\n}\n'
    client.post("/api/v1/type/delete/1")
    res = client.post("/api/v1/type/attribute/delete/1")
    assert res.data == b'{\n  "msg": "",\n  "wasAllowed": true\n}\n'


# Checks to see if an attribute name is in the database
def test_is_attr_name_in(client):
    test_attribute = {
        "attributeName": "public",
        "attributeType": "checkbox",
    }
    client.post("/api/v1/type/adder/new", json=test_attribute)
    res = client.post("/api/v1/type/adder/isAttrNameIn",
                      json={"name": "public"})
    assert res.status_code == 200
    assert res.data == b'{\n  "data": true\n}\n'
    res = client.post("/api/v1/type/adder/isAttrNameIn",
                      json={"name": "private"})
    assert res.data == b'{\n  "data": false\n}\n'
