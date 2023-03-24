import json
import os
from datetime import datetime

import pytest

from app.db import Actions, Models


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1, "add_to_db": True}],
    indirect=True,
)
def test_logs(db_conn, valid_client, new_assets):
    with db_conn.cursor() as cur:
        cur.execute(
            """INSERT INTO audit_logs (model_id,account_id,object_id,diff,action)
    VALUES (%(model_id)s,%(account_id)s,%(object_id)s,%(diff)s,%(action)s);""",
            {
                "model_id": int(Models.ASSETS),
                "account_id": 1,
                "object_id": new_assets[0].asset_id,
                "diff": json.dumps({}),
                "action": Actions.ADD,
            },
        )
        db_conn.commit()
    res = valid_client.get(f"/api/v1/asset/logs/{new_assets[0].asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"] == 1
    assert res.json["data"][0]["action"] == "ADD"
    assert res.json["data"][0]["diff"] == {}
    assert res.json["data"][0]["logID"] == 1
    assert res.json["data"][0]["modelID"] == int(Models.ASSETS)
    assert res.json["data"][0]["objectID"] == 1
    assert res.json["data"][0]["username"] == os.environ["DEFAULT_SUPERUSER_USERNAME"]
    assert datetime.fromisoformat(res.json["data"][0]["date"]) < datetime.now()


@pytest.mark.parametrize(
    "new_assets",
    [{"batch_size": 1}],
    indirect=True,
)
def test_logs_add(valid_client, new_assets):
    data = json.loads(new_assets[0].json(by_alias=True))
    res = valid_client.post("/api/v1/asset/", json=data)
    assert res.status_code == 201
    asset_id = res.json["data"]
    res = valid_client.get(f"/api/v1/asset/logs/{asset_id}")
    assert res.status_code == 200
    assert res.json["data"][0]["accountID"] == 1
    assert res.json["data"][0]["action"] == "ADD"
    assert res.json["data"][0]["diff"] == {"added": list(data.keys())}
    assert res.json["data"][0]["logID"] == 1
    assert res.json["data"][0]["modelID"] == int(Models.ASSETS)
    assert res.json["data"][0]["objectID"] == 1
    assert res.json["data"][0]["username"] == os.environ["DEFAULT_SUPERUSER_USERNAME"]
    assert datetime.fromisoformat(res.json["data"][0]["date"]) < datetime.now()
