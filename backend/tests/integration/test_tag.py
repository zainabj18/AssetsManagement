from unittest import mock

from psycopg import Error
from psycopg.rows import dict_row


def test_tag_create_requires_name(client):
    res = client.post("/api/v1/tag/", json={})
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {"loc": ["name"], "msg": "field required", "type": "value_error.missing"}
        ],
        "error": "Failed to create tag from the data provided",
        "msg": "Data provided is invalid",
    }


def test_tag_create_adds_to_db(client, db_conn):
    res = client.post("/api/v1/tag/", json={"name": "Test"})
    assert res.status_code == 200
    expected = {"id": 1, "name": "Test"}
    assert res.json == {"data": expected, "msg": "Tag Created"}

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""SELECT * FROM tags WHERE name=%(name)s;""", expected)
        tag = cur.fetchone()
        assert tag["id"] == expected["id"]
        assert tag["name"] == expected["name"]


def test_tag_create_db_error(client):
    with mock.patch(
        "app.tag.routes.create_tag", side_effect=Error("Fake error executing query")
    ) as p:
        res = client.post("/api/v1/tag/", json={"name": "Test"})

        assert res.status_code == 500
        p.assert_called()
        assert res.json == {
            "error": "Database Error",
            "msg": "Fake error executing query",
        }


def test_tag_duplicate_name(client):
    res = client.post("/api/v1/tag/", json={"name": "Test"})
    assert res.status_code == 200
    expected = {"id": 1, "name": "Test"}
    assert res.json == {"data": expected, "msg": "Tag Created"}
    res = client.post("/api/v1/tag/", json={"name": "Test"})
    assert res.status_code == 500
    assert res.json == {"error": "Database Error", "msg": "Tag Test already exists"}


def test_tag_list(client):
    expected_results = []
    for x in range(100):
        name = f"Test-{x}"
        res = client.post("/api/v1/tag/", json={"name": name})
        assert res.status_code == 200
        expected_results.append({"id": x + 1, "name": name})
    res = client.get("/api/v1/tag/")
    assert res.status_code == 200
    assert res.json == {"msg": "tags", "data": expected_results}


def test_tag_list_db_error(client):
    res = client.post("/api/v1/tag/", json={"name": "Tes"})
    assert res.status_code == 200
    with mock.patch(
        "app.tag.routes.list_tags", side_effect=Error("Fake error executing query")
    ) as p:
        res = client.get("/api/v1/tag/")

        assert res.status_code == 500
        p.assert_called()
        assert res.json == {
            "error": "Database Error",
            "msg": "Fake error executing query",
        }

def test_tag_delete(valid_client,db_conn):
    res = valid_client.post("/api/v1/tag/", json={"name": "Test"})
    expected = {"id": 1, "name": "Test"}
    assert res.status_code == 200
    assert res.json == {"data": expected, "msg": "Tag Created"}
    res = valid_client.delete(f"/api/v1/tag/{1}")
    assert res.status_code == 200
    with db_conn.cursor() as cur:
        cur.execute(
            """SELECT * FROM tags WHERE id=%(id)s;""",
            {"id": 1},
        )
        assert cur.fetchall()==[]

def test_tag_delete_db_error(valid_client,db_conn):
    res = valid_client.post("/api/v1/tag/", json={"name": "Test"})
    expected = {"id": 1, "name": "Test"}
    assert res.status_code == 200
    assert res.json == {"data": expected, "msg": "Tag Created"}
    with mock.patch(
        "app.tag.routes.delete_tag", side_effect=Error("Fake error executing query")
    ) as p:
        res = valid_client.delete(f"/api/v1/tag/{1}")
        assert res.status_code == 500
        p.assert_called()
        assert res.json == {
            "error": "Database Error",
            "msg": "Fake error executing query",
        }
        with db_conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM tags WHERE id=%(id)s;""",
                {"id": 1},
            )
            assert cur.fetchall()!=[]