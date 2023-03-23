from psycopg.rows import dict_row


def test_project_list(client, db_conn):
    expected_projects = []
    with db_conn.cursor() as cur:
        for x in range(100):
            name = f"Test-{x}"
            project = {"name": name, "description": name}
            cur.execute(
                """
                INSERT INTO projects (name,description)
                VALUES (%(name)s,%(description)s) RETURNING id;
                """,
                project,
            )
            id = cur.fetchone()[0]
            project["id"] = id
            expected_projects.append(project)
        db_conn.commit()
    res = client.get("/api/v1/project/")
    assert res.status_code == 200
    for i in range(0, len(expected_projects)):
         assert res.json["data"][i]["projectName"] == expected_projects[i]["name"]
         assert res.json["data"][i]["projectDescription"] == expected_projects[i]["description"]


def test_get_project(client, db_conn):
    q1 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('john','mark','john123','321')"""
    q2 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('sam','johnstone','sam69','123')"""
    q3 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('Taka','Minamino','taka12','690')"""
    q4 = """INSERT INTO people_in_projects (account_id, project_id) VALUES (%(account)s, %(project)s)"""
    with db_conn.connection as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO projects(name, description, type) VALUES ('TestProject', 'This is a test project', 'PUBLIC');""")
            cur.execute(q1)
            cur.execute(q2)
            cur.execute(q3)
            cur.execute(q4,{"account": 1,"project": 1})
            cur.execute(q4,{"account": 2,"project": 1})
            cur.execute(q4,{"account": 3,"project": 1})

    
    res = client.get("/api/v1/project/1")

    assert res.status_code == 200

    expected_data = {
        "projectName": "TestProject",
        "projectDescription": "This is a test project",
        "projectType": "PUBLIC",
        "linkedAccounts": [1, 2, 3]
    }
    print(res.json)
    assert res.json['data']['projectName'] == expected_data['projectName']
    assert res.json['data']['projectDescription'] == expected_data['projectDescription']
    assert res.json['data']['projectType'] == expected_data['projectType']
    assert res.json['data']['linkedAccounts'] == expected_data['linkedAccounts']





def test_project_route(client, db_conn):
    test_project = {
        "name": "Project1",
        "description": "New Project",
        "accounts": [2,3,4]
    }
    q1 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('john','mark','john123','321')"""
    q2 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('sam','johnstone','sam69','123')"""
    q3 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('Taka','Minamino','taka12','690')"""
    with db_conn as conn: 
        conn.execute(q1)
        conn.execute(q2)
        conn.execute(q3)
    res = client.post("/api/v1/project/new", json=test_project)
    assert res.status_code == 200

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM projects WHERE name=%(name)s AND description=%(description)s;""",
            {"name": test_project["name"], "description": test_project["description"]},
        )
        project = cur.fetchone()
        assert project["name"] == test_project["name"]
        assert project["description"] == test_project["description"]