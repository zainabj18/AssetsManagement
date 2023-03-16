from app.db import get_db
from flask import Blueprint

bp = Blueprint("graphs", __name__, url_prefix="/graph")

@bp.route("/assets", methods=["GET"])
def get_assets():
    query = """
    SELECT asset_id, name
    FROM assets;
    """
    sub_query = """
    SELECT to_asset_id
    FROM assets_in_assets
    WHERE from_asset_id = %(from)s;
    """
    db = get_db()
    with db.connection() as conn:
        res = conn.execute(query)
        assets = res.fetchall()
        for i, tup in enumerate(assets):
            assets[i] = {"id": tup[0], "name": tup[1]}
        data = []
        for asset in assets:
            asset_id = asset["id"]
            res = conn.execute(sub_query, {"from" : asset_id})
            to = res.fetchall()
            for i, item in enumerate(to):
                to[i] = item[0]
            data.append({"from": asset_id ,"to": to})
    return {"data": {"points": assets, "joins": data}}, 200