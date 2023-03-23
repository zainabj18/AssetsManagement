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
         print(res.json["data"][i])
         assert res.json["data"][i]["projectName"] == expected_projects[i]["name"]
         assert res.json["data"][i]["projectDescription"] == expected_projects[i]["description"]


def test_get_project(client, db_conn):
    with db_conn.connection as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO projects(name, description) VALUES ('TestProject', 'This is a test project');""")
    
    res = client.get("/api/v1/project/1")

    assert res.status_code == 200

    expected_data = {
        "projectName": "TestProject",
        "projectDescription": "This is a test project",
    }
    assert res.json['data']['projectName'] == expected_data['projectName']
    assert res.json['data']['projectDescription'] == expected_data['projectDescription']




def test_project_route(client, db_conn):
    test_project = {
        "name": "Project1",
        "description": "New Project",
    }
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