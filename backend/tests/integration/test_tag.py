from unittest import mock
from psycopg import Error
from psycopg.rows import dict_row
from app.db import UserRole, DataAccess
from tests.factories import TagFactory
import pytest

def create_tags_in_db(db_conn,size=1,**kwargs):
    tags=TagFactory.batch(size,**kwargs)
    tags_in_db=[]
    with db_conn.cursor() as cur:
        for tag in tags:
            cur.execute(
                """
            INSERT INTO tags (id,name)
    VALUES (%(id)s,%(name)s) ON CONFLICT DO NOTHING RETURNING id;""",
                tag.dict(),
            )
            if db_id := cur.fetchone():
                tag.id=db_id[0]
                print("tag in db")
                print(tag.id)
                tags_in_db.append(tag.dict())
        db_conn.commit()
    return tags_in_db


def test_tag_create_requires_name(valid_client):
    res = valid_client.post("/api/v1/tag/", json={})
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {"loc": ["name"], "msg": "field required", "type": "value_error.missing"}
        ],
        "error": "Failed to create tag from the data provided",
        "msg": "Data provided is invalid",
    }


def test_tag_create_requires_name_not_to_empty(valid_client):

    res = valid_client.post("/api/v1/tag/", json={"name": ""})
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "ctx": {"limit_value": 1},
                "loc": ["name"],
                "msg": "ensure this value has at least 1 characters",
                "type": "value_error.any_str.min_length",
            }
        ],
        "error": "Failed to create tag from the data provided",
        "msg": "Data provided is invalid",
    }


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC}),
        ({"account_type": UserRole.USER, "account_privileges": DataAccess.PUBLIC}),
    ],
    indirect=True,
)
def test_tag_create_adds_to_db(valid_client, db_conn):
    res = valid_client.post("/api/v1/tag/", json={"name": "Test"})
    assert res.status_code == 200
    expected = {"id": 1, "name": "Test"}
    assert res.json == {"data": expected, "msg": "Tag Created"}

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""SELECT * FROM tags WHERE name=%(name)s;""", expected)
        tag = cur.fetchone()
        assert tag["id"] == expected["id"]
        assert tag["name"] == expected["name"]


def test_tag_create_db_error(valid_client):
    with mock.patch(
        "app.tag.routes.create_tag", side_effect=Error("Fake error executing query")
    ) as p:
        res = valid_client.post("/api/v1/tag/", json={"name": "Test"})

        assert res.status_code == 500
        p.assert_called()
        assert res.json == {
            "error": "Database Error",
            "msg": "Fake error executing query",
        }


def test_tag_duplicate_name(valid_client):
    res = valid_client.post("/api/v1/tag/", json={"name": "Test"})
    assert res.status_code == 200
    expected = {"id": 1, "name": "Test"}
    assert res.json == {"data": expected, "msg": "Tag Created"}
    res = valid_client.post("/api/v1/tag/", json={"name": "Test"})
    assert res.status_code == 500
    assert res.json == {"error": "Database Error", "msg": "Tag Test already exists"}


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC}),
        ({"account_type": UserRole.USER, "account_privileges": DataAccess.PUBLIC}),
        ({"account_type": UserRole.VIEWER, "account_privileges": DataAccess.PUBLIC}),
    ],
    indirect=True,
)
def test_tag_list_from_db(valid_client, db_conn):
    expected_results = create_tags_in_db(db_conn,100)
    res = valid_client.get("/api/v1/tag/")
    assert res.status_code == 200
    assert res.json == {"msg": "tags", "data": expected_results}


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC}),
        ({"account_type": UserRole.USER, "account_privileges": DataAccess.PUBLIC}),
    ],
    indirect=True,
)
def test_tag_list_from_post(valid_client):
    expected_results = []
    for x in range(100):
        name = f"Test-{x}"
        res = valid_client.post("/api/v1/tag/", json={"name": name})
        assert res.status_code == 200
        expected_results.append({"id": x + 1, "name": name})
    res = valid_client.get("/api/v1/tag/")
    assert res.status_code == 200
    assert res.json == {"msg": "tags", "data": expected_results}


def test_tag_list_db_error(valid_client):
    res = valid_client.post("/api/v1/tag/", json={"name": "Tes"})
    assert res.status_code == 200
    with mock.patch(
        "app.tag.routes.list_tags", side_effect=Error("Fake error executing query")
    ) as p:
        res = valid_client.get("/api/v1/tag/")

        assert res.status_code == 500
        p.assert_called()
        assert res.json == {
            "error": "Database Error",
            "msg": "Fake error executing query",
        }


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC}),
        ({"account_type": UserRole.USER, "account_privileges": DataAccess.PUBLIC}),
    ],
    indirect=True,
)
def test_tag_delete(valid_client, db_conn):
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
        assert cur.fetchall() == []


def test_tag_delete_db_error(valid_client, db_conn):
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
            assert cur.fetchall() != []


@pytest.mark.parametrize(
    "valid_client",
    [{"account_type": UserRole.VIEWER, "account_privileges": DataAccess.PUBLIC}],
    indirect=True,
)
def test_tag_viewer_cannot_create(valid_client):
    res = valid_client.post("/api/v1/tag/", json={"name": "Test"})
    assert res.status_code == 403
    assert res.json == {
        "error": "Invalid Token",
        "msg": "Your account is forbidden to access this please speak to your admin",
    }


@pytest.mark.parametrize(
    "valid_client",
    [{"account_type": UserRole.VIEWER, "account_privileges": DataAccess.PUBLIC}],
    indirect=True,
)
def test_tag_viewer_cannot_delete(valid_client):
    res = valid_client.delete(f"/api/v1/tag/{1}")
    assert res.status_code == 403
    assert res.json == {
        "error": "Invalid Token",
        "msg": "Your account is forbidden to access this please speak to your admin",
    }


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_tag_delete_with_assets(valid_client, new_assets,db_conn):
    tags = []
    for asset in new_assets:
        tags.extend(asset.tags)
    tags=set(tags)
    for tag in tags:
        res = valid_client.delete(f"/api/v1/tag/{tag}")
        assert res.status_code == 200
        with db_conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM assets_in_tags WHERE tag_id=%(id)s;""",
                {"id": tag},
            )
            assert cur.fetchall()==[]

def test_tag_copy_to_requires_tag_id(valid_client):
    res = valid_client.post("/api/v1/tag/copy", json={})
    assert res.status_code == 400
    assert {
                "loc": ["to_tag_id"],
                "msg": "field required",
                "type": "value_error.missing",
            } in res.json["data"]
    assert res.json["error"]=="Failed to copy to tag from the data provided"
    assert res.json["msg"]=="Data provided is invalid"

def test_tag_copy_to_requires_assest_ids_list(valid_client):
    res = valid_client.post("/api/v1/tag/copy", json={})
    assert res.status_code == 400
    assert {
                "loc": ["assest_ids"],
                "msg": "field required",
                "type": "value_error.missing",
            } in res.json["data"]
    assert res.json["error"]=="Failed to copy to tag from the data provided"
    assert res.json["msg"]=="Data provided is invalid"

def test_tag_copy_to_requires_tag_id_int(valid_client):
    res = valid_client.post("/api/v1/tag/copy", json={"to_tag_id":"j"})
    assert res.status_code == 400
    assert {
                "loc": ["to_tag_id"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            } in res.json["data"]
    assert res.json["error"]=="Failed to copy to tag from the data provided"
    assert res.json["msg"]=="Data provided is invalid"

def test_tag_copy_to_requires_assest_ids_list(valid_client):
    res = valid_client.post("/api/v1/tag/copy", json={"assest_ids":"j"})
    assert res.status_code == 400
    assert {
                "loc": ["assest_ids"],
                "msg": 'value is not a valid list',
                "type": "type_error.list",
            } in res.json["data"]
    assert res.json["error"]=="Failed to copy to tag from the data provided"
    assert res.json["msg"]=="Data provided is invalid"

def test_tag_copy_to_requires_assest_ids_list_ints(valid_client):
    res = valid_client.post("/api/v1/tag/copy", json={"assest_ids":["j",1]})
    assert res.status_code == 400
    assert {
                "loc": ['assest_ids', 0],
                "msg":'value is not a valid integer',
                "type": "type_error.integer",
            } in res.json["data"]
    assert res.json["error"]=="Failed to copy to tag from the data provided"
    assert res.json["msg"]=="Data provided is invalid"

def test_tag_copy_to_requires_valid_to_tag_id(valid_client):
    res = valid_client.post("/api/v1/tag/copy", json={"to_tag_id":1,"assest_ids":[1]})
    assert res.status_code == 400
    assert res.json=={'data': 1, 'error': "Tag with 1 doesn't exist", 'msg': 'Data provided is invalid'}


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 100,"add_to_db":True}],
    indirect=True,
)
def test_tag_copy_db_change(valid_client,db_conn,new_assets):
    new_tags = create_tags_in_db(db_conn,1,id=100,name="t")
    asset_ids=[asset.asset_id for asset in new_assets]
    res = valid_client.post("/api/v1/tag/copy", json={"to_tag_id":100,"assest_ids":asset_ids})
    assert res.status_code == 200
    assert res.json=={"msg":"Copied assets to tag"}
    with db_conn.cursor() as cur:
        cur.execute("""SELECT asset_id FROM assets_in_tags WHERE tag_id=%(id)s;""", {"id":100})
        assert asset_ids==[row[0] for row in cur.fetchall()]