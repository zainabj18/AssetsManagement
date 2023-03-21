import pytest

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

# @pytest.mark.parametrize(
#     "new_assets",
#     [{"batch_size": 1,"add_to_db":True}],
#     indirect=True,
# )
# @pytest.mark.parametrize(
#     "type_verions",
#     [{"size": 10,"add_to_db": True}],
#     indirect=True,
# )
# def test_upgrade_availiable(db_conn,valid_client,new_assets,type_verions):
#     print(type(new_assets[0]))
#     with db_conn.cursor() as cur:
#         cur.execute("SELECT type_id FROM type_version WHERE version_id=%(version_id)s",{"version_id":new_assets[0].version_id})
#         type_id=cur.fetchone()[0]
#         cur.execute(
#             """UPDATE type_version
# SET type_id = %(type_id)s""",
#             {"type_id": type_id},
#         )
#         min_version_number=min([row.version_number for row in type_verions[0]])
#         cur.execute(
#             """UPDATE type_version
# SET version_number = %(version_number)s WHERE version_id=%(version_id)s""",
#             {"version_number":min_version_number-1,"version_id":new_assets[0].version_id},
#         )
#         cur.execute(
#             """SELECT MAX(version_id) FROM type_version;""")
#         db_conn.commit()
#         max_version_id=cur.fetchone()[0]
#         max_version_attributes_id=[]
#         max_version_attributes=[]
#         for row in type_verions[0]:
#             if row.version_id==max_version_id:
#                 for attribute in row.attributes:
#                     max_version_attributes_id.append(attribute.attribute_id)
#                     max_version_attributes.append(attribute)
#         print(max_version_attributes_id)
#         cur.execute(
#             """SELECT attribute_id FROM attributes_in_types WHERE type_version=%(type_version)s ;""",{"type_version":new_assets[0].version_id})
#         old_version_attributes_id=[row[0] for row in cur.fetchall()]
#         res = valid_client.get(f"/api/v1/asset/upgrade/{new_assets[0].asset_id}")
#         assert res.status_code == 200
#         assert res.json["msg"] == "upgrade needed"
#         assert res.json["canUpgrade"]==True
#         assert len(res.json["data"])==3
#         new_attributes_counter=0
#         for a in max_version_attributes:
#             if a.attribute_id not in old_version_attributes_id:
#                 att=a.dict(by_alias=True,exclude={"attribute_value"}) 
#                 assert att in res.json["data"][0]
#                 new_attributes_counter+=1
#             else:
#                 old_version_attributes_id.remove(a.attribute_id)
#         assert len(res.json["data"][0])==new_attributes_counter
#         print(old_version_attributes_id)
#         cur.execute(
#             """SELECT attribute_name FROM attributes WHERE attribute_id=ANY(%(attribute_ids)s);""",{"attribute_ids":old_version_attributes_id})
#         removed_names=[row[0] for row in cur.fetchall()]

#         print(removed_names)
#         assert set(res.json["data"][1])==set(removed_names)
#         assert res.json["data"][2]==max_version_id


