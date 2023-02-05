from psycopg.rows import dict_row
from unittest import mock
from psycopg import Error
def test_tag_create_requires_name(client):
    res = client.post("/api/v1/tag/",json={})
    assert res.status_code == 400
    assert res.json=={'data': [{'loc': ['name'],
                    'msg': 'field required',
                    'type': 'value_error.missing'}],
            'error': 'Failed to create tag from the data provided',
            'msg': 'Data provided is invalid'}

def test_tag_create_adds_to_db(client,db_conn):
    res = client.post("/api/v1/tag/",json={"name":"Test"})
    assert res.status_code == 200
    expected={"id":1,"name":"Test"}
    assert res.json=={'data': expected,
            'msg': 'Tag Created'}

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM tags WHERE name=%(name)s;""", expected
        )
        tag = cur.fetchone()
        assert tag["id"] == expected["id"]
        assert tag["name"] == expected["name"]

def test_tag_create_db_error(client):
    with mock.patch(
            "app.tag.routes.create_tag", side_effect=Error("Fake error executing query")
        ) as p:
        res = client.post("/api/v1/tag/",json={"name":"Test"})
        
        assert res.status_code == 500
        p.assert_called()
        assert res.json=={
            "error": "Database Connection Error",
            "msg": "Fake error executing query",
        }
        