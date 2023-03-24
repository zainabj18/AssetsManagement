def test_get_users(client, db_conn):

    q1 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('john','mark','john123','321')"""
    q2 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('sam','johnstone','sam69','123')"""
    q3 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('jo','Minamino','jo12','690')"""
    with db_conn as conn:
        conn.execute(q1)
        conn.execute(q2)
        conn.execute(q3)
    res = client.get("/api/v1/admin/accountmanager")
    assert res.status_code == 200
    assert res.json["data"][1]["username"] == "john123"
    assert res.json["data"][2]["username"] == "sam69"
    assert res.json["data"][3]["username"] == "jo12"

    assert res.json["data"][1]["lastName"] == "mark"
    assert res.json["data"][2]["lastName"] == "johnstone"
    assert res.json["data"][3]["lastName"] == "Minamino"

    assert res.json["data"][1]["firstName"] == "john"
    assert res.json["data"][2]["firstName"] == "sam"
    assert res.json["data"][3]["firstName"] == "jo"
