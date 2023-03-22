import pytest
from app.db import Models,Actions
from psycopg.rows import dict_row
from app.schemas.factories import CommentFactory
from datetime import datetime,timedelta
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_add_requires_comment(valid_client, new_assets):
    res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json={})
    assert res.status_code == 400
    assert res.json["msg"]=="Failed to add comment from the data provided"
    assert res.json["error"]=="Invalid data"
    assert {
        "loc": ["comment"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]

def test_comment_add_requires_asset_in_db(valid_client):
    res = valid_client.post(f"/api/v1/asset/comment/{1}",json={"comment":"Hello World!"})
    assert res.status_code == 404
    assert res.json["msg"]=="Asset doesn't exist"

def test_comment_add_requires_comment(valid_client):
    res = valid_client.post(f"/api/v1/asset/comment/{1}",json={})
    assert res.status_code == 400
    assert res.json["msg"]=="Failed to add comment from the data provided"
    assert {
        "loc": ["comment"],
        "msg": "field required",
        "type": "value_error.missing",
    } in res.json["data"]

def test_comment_require_not_empty(valid_client):
    res = valid_client.post(f"/api/v1/asset/comment/{1}",json={"comment":""})
    assert res.status_code == 400
    assert res.json["msg"]=="Failed to add comment from the data provided"
    assert {'ctx': {'limit_value': 1}, 'loc': ['comment'], 'msg': 'ensure this value has at least 1 characters', 'type': 'value_error.any_str.min_length'} in res.json["data"]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_add_to_db(db_conn,valid_client, new_assets):
    comment="Hello World!"
    res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json={"comment":comment})
    assert res.status_code == 200
    assert res.json["msg"]=="Comment added"
    with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
            SELECT * FROM comments WHERE asset_id=%(id)s""",
                {"id":new_assets[0].asset_id}
            )
            added_comment=cur.fetchone()
            assert added_comment["account_id"]==1
            assert added_comment["asset_id"]==new_assets[0].asset_id
            assert added_comment["comment"]==comment
            assert added_comment["datetime"]<datetime.utcnow()
            assert added_comment["datetime"]>(datetime.utcnow()-timedelta(minutes=2))

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_multiple(db_conn,valid_client, new_assets):
    comments=CommentFactory.batch(size=100)
    comment_values=[]
    for comment in comments:
        comment_values.append(comment.comment)
        res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json=comment.dict())
        assert res.status_code == 200
        assert res.json["msg"]=="Comment added"
    
    with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
            SELECT * FROM comments WHERE asset_id=%(id)s""",
                {"id":new_assets[0].asset_id}
            )
            added_comments=cur.fetchall()
            assert len(added_comments)==len(comments)
            for db_comment in added_comments:
                assert db_comment["account_id"]==1
                assert db_comment["asset_id"]==new_assets[0].asset_id
                comment_values.remove(db_comment["comment"])
                assert db_comment["datetime"]<datetime.utcnow()
                assert db_comment["datetime"]>(datetime.utcnow()-timedelta(minutes=2))
            assert len(comment_values)==0

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_get(db_conn,valid_client, new_assets):
    comments=CommentFactory.batch(size=100)
    comment_values=[]
    for comment in comments:
        comment_values.append(comment.comment)
        res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json=comment.dict())
        assert res.status_code == 200
        assert res.json["msg"]=="Comment added"
    res = valid_client.get(f"/api/v1/asset/comment/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert res.json["msg"]=="Comments"
    assert len(res.json["data"])==len(comments)
    for index,comment in enumerate(comments):
        db_comment=res.json["data"][index]
        assert db_comment["accountID"]==1
        assert db_comment["assetID"]==new_assets[0].asset_id
        comment_values.remove(db_comment["comment"])
    assert len(comment_values)==0  


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_add_logged(db_conn,valid_client, new_assets):
    comment="Hello World!"
    res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json={"comment":comment})
    assert res.status_code == 200
    assert res.json["msg"]=="Comment added"
    with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
            SELECT * FROM audit_logs WHERE object_id=%(asset_id)s AND model_id=%(model_id)s""",
                {"asset_id":new_assets[0].asset_id,"model_id":Models.ASSETS}
            )
            logs=cur.fetchone()
            assert logs["model_id"]==Models.ASSETS
            assert logs["action"]==Actions.ADD
            assert logs["diff"]=={'added': ['comment']}
            assert logs["account_id"]==1

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_comment_delete(db_conn,valid_client, new_assets):
    comment="Hello World!"
    res = valid_client.post(f"/api/v1/asset/comment/{new_assets[0].asset_id}",json={"comment":comment})
    assert res.status_code == 200
    res = valid_client.delete(f"/api/v1/asset/comment/{new_assets[0].asset_id}/remove/{1}")
    assert res.status_code == 200
    assert res.json["msg"]=="Comment deleted"
    with db_conn.cursor() as cur:
        cur.execute(
            """SELECT * FROM comments WHERE comment_id=%(id)s;""",
            {"id": 1},
        )
        assert cur.fetchall()==[]

