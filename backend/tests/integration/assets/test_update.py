import pytest
import json
from app.db import DataAccess,UserRole
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
def test_upgrade_not_availiable(db_conn,valid_client,new_assets,type_verions):
    res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert res.json["msg"] == "no upgrade needed"
    assert res.json["data"]==[]

@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1,"add_to_db":True}],
    indirect=True,
)
@pytest.mark.parametrize(
    "type_verions",
    [{"size": 10,"add_to_db": True}],
    indirect=True,
)
def test_upgrade_availiable(db_conn,valid_client,new_assets,type_verions):
    with db_conn.cursor() as cur:
        # update type_version so every verion in db corresponds to asset's type
        lastest_type_version=type_verions["added"][-1]
        cur.execute(
            """UPDATE type_version
SET type_id = %(type_id)s WHERE version_id=%(version_id)s""",
            {"type_id": lastest_type_version.type_id,"version_id":new_assets[0].version_id}
        )
        cur.execute(
                """
    INSERT INTO type_version_link (type_version_from, type_version_to)
    VALUES (%(from)s, %(to)s)
    """,
                {"from": lastest_type_version.version_id,"to":new_assets[0].version_id},
            )
        db_conn.commit()
        res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
        assert res.status_code == 200
        assert res.json["msg"] == "upgrade needed"
        # get all old attributes
        cur.execute(
            """SELECT attribute_id FROM attributes_in_types WHERE type_version=%(type_version)s ;""",{"type_version":new_assets[0].version_id})
        old_version_attributes_id=[row[0] for row in cur.fetchall()]
        new_attributes_counter=0
        # check new attribute returned 
        for a in lastest_type_version.attributes:
            if a.attribute_id not in old_version_attributes_id:
                att=a.dict(by_alias=True,exclude={"attribute_value"}) 
                assert att in res.json["data"]["addedAttributes"]
                new_attributes_counter+=1
            else:
                old_version_attributes_id.remove(a.attribute_id)
        assert len(res.json["data"]["addedAttributes"])==new_attributes_counter
        # check that old attribute returned
        cur.execute(
            """SELECT attribute_name FROM attributes WHERE attribute_id=ANY(%(attribute_ids)s);""",{"attribute_ids":old_version_attributes_id})
        removed_names=[row[0] for row in cur.fetchall()]
        assert set(res.json["data"]["removedAttributesNames"])==set(removed_names)
        # check that depencdencies updated
        cur.execute(
            """SELECT type_name FROM type_names_versions WHERE version_id=%(version_id)s;""",{"version_id":new_assets[0].version_id})
        assert set(cur.fetchone())==set(res.json["data"]["dependsOn"])
        assert len(res.json["data"]["dependsOn"])==1
        # check new version id given
        assert res.json["data"]["maxVersion"]==lastest_type_version.version_id



def test_new_assets_get_invalid_id(valid_client):
    res = valid_client.get(f"/api/v1/asset/upgrade/{1}")
    assert res.status_code == 404
    assert res.json=={'msg': "Asset doesn't exist"}


@pytest.mark.parametrize(
    "valid_client",
    [
        ({"account_type": UserRole.ADMIN, "account_privileges": DataAccess.PUBLIC})
    ],
    indirect=True,
)
@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_new_assets_get_account_privileges_check(valid_client, new_assets):
    new_assets[0].classification=DataAccess.CONFIDENTIAL
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    assert res.json["msg"] == "Added asset"
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/upgrade/{asset_id}")
    assert res.status_code == 403
    assert res.json=={'msg': 'Your account is forbidden to access this please speak to your admin'}

