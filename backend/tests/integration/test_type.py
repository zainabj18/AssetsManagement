# Test for the path to the type adder
def test_typeAdder_route(client):
    res = client.get("/api/v1/type/adder")
    assert res.status_code == 200


def test_type_list(client,db_conn):
    expected_types=[]
    with db_conn.cursor() as cur:
        for x in range(100):
            name=f"Test-{x}"
            type={'name': name}
            cur.execute(
        """
    INSERT INTO types (name)
VALUES (%(name)s) RETURNING id;""",
        type,
    )
            id=cur.fetchone()[0]
            type['id']=id
            expected_types.append(type)
        db_conn.commit()
    res = client.get("/api/v1/type/")
    assert res.status_code == 200
    assert res.json=={"msg": "types","data":expected_types}
