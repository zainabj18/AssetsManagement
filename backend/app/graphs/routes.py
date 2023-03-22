from app.db import get_db
from flask import Blueprint
import math
from colorutils import random_web
bp = Blueprint("graphs", __name__, url_prefix="/graph")


# Returns the first item in each index of the given 2D list
def remove_end(li):
    for i, item in enumerate(li):
        li[i] = item[0]
    return li


# Returns the json of a 2d list [[id, name]]
def extract_name_id(li):
    for i, tup in enumerate(li):
        li[i] = {"id": tup[0], "name": tup[1],"version_id": tup[2]}
    return li

VERSION_ID_COLOURS_DICT={}
@bp.route("/assets", methods=["GET"])
def get_assets():
    query = """
    SELECT asset_id, name,version_id
    FROM assets;
    """
    sub_query_1 = """
    SELECT to_asset_id
    FROM assets_in_assets
    WHERE from_asset_id = %(from)s;
    """
    sub_query_2 = """
    SELECT from_asset_id
    FROM assets_in_assets
    WHERE to_asset_id = %(to)s;
    """
    db = get_db()
    with db.connection() as conn:
        res = conn.execute(query)
        assets = extract_name_id(res.fetchall())
        data = []
        for asset in assets:
            asset_id = asset["id"]
            res = conn.execute(sub_query_1, {"from": asset_id})
            to = remove_end(res.fetchall())
            
            if asset["version_id"] not in VERSION_ID_COLOURS_DICT:
                VERSION_ID_COLOURS_DICT[asset["version_id"]]=random_web()
            asset["color"]=VERSION_ID_COLOURS_DICT[asset["version_id"]]
            print(to)
            # for x in to:
            #     data.append({"source": asset_id, "target": x,"linkColor":"red"})

            res = conn.execute(sub_query_2, {"to": asset_id})
            from_assets = remove_end(res.fetchall())
            for x in from_assets:
                data.append({"source": x, "target": asset_id,"linkColor":"blue"})
            asset["degree"]=len(from_assets)
            asset["size"]=1+math.log(asset["degree"]+1)
    return {"nodes": assets, "links": data}, 200

@bp.route("/asset/<id>", methods=["GET"])
def get_asset(id):
    try:
        id = int(id)
    except ValueError:
        return {"data": {"points": [], "joins": []}, "msg": "Given id was not an int."}, 400
    query_from = """
    SELECT to_asset_id
    FROM assets_in_assets
    WHERE from_asset_id = %(from)s;
    """
    query_to = """
    SELECT from_asset_id
    FROM assets_in_assets
    WHERE to_asset_id = %(to)s;
    """
    query_name = """
    SELECT name
    FROM assets
    WHERE asset_id = %(id)s;
    """
    db = get_db()
    with db.connection() as conn:
        data = []
        assetList = [id]
        res = conn.execute(query_from, {"from": id})
        id_from = remove_end(res.fetchall())
        data.append({"from": id, "to": id_from})
        for asset in id_from:
            if asset not in assetList:
                assetList.append(asset)
        res = conn.execute(query_to, {"to": id})
        to_ids = res.fetchall()
        for asset in to_ids:
            asset_id = asset[0]
            data.append({"from": asset_id, "to": [id]})
            if asset_id not in assetList:
                assetList.append(asset_id)

        points = []
        for key in assetList:
            res = conn.execute(query_name, {"id": key})
            points.append({"id": key, "name": res.fetchone()[0]})
    return {"data": {"points": points, "joins": data}}, 200


@bp.route("/types", methods=["GET"])
def get_types():
    query = """
    SELECT version_id, type_name
    FROM type_version AS v1
    INNER JOIN types as t ON v1.type_id = t.type_id
    WHERE version_number = 
    (
        SELECT MAX(v2.version_number)
        FROM type_version as v2
        WHERE v1.type_id = v2.type_id
    )
    GROUP BY v1.type_id, version_id, type_name;
    """
    sub_query = """
    SELECT type_version_to
    FROM type_version_link
    WHERE type_version_from = %(from)s;
    """
    db = get_db()
    with db.connection() as conn:
        res = conn.execute(query)
        types = res.fetchall()
        for i, tup in enumerate(types):
            types[i] = {"id": tup[0], "name": tup[1]}
        data = []
        for type in types:
            version_id = type["id"]
            res = conn.execute(sub_query, {"from": version_id})
            to = remove_end(res.fetchall())
            data.append({"from": version_id, "to": to})
    return {"data": {"points": types, "joins": data}}, 200
