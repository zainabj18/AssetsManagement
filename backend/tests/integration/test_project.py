from unittest import mock

from psycopg import Error
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


# def test_projects_list_db_error(client):
#     with mock.patch(
#         "app.project.routes.get_projects",
#         side_effect=Error("Fake error executing query"),
#     ) as p:
#         res = client.get("/api/v1/project/")

#         assert res.status_code == 500
#         p.assert_called()
#         assert res.json == {
#             "error": "Database Error",
#             "msg": "Fake error executing query",
#         }


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


def test_get_project_account(client,db_conn):
    test_project = {
        "name": "Project1",
        "description": "New Project",
        "accounts": [2,3]
    }
    q1 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('john','mark','john123','321')"""
    q2 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('sam','johnstone','sam69','123')"""
    q3 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('Taka','Minamino','taka12','690')"""
    with db_conn as conn: 
        conn.execute(q1)
        conn.execute(q2)
        conn.execute(q3)
    client.post("/api/v1/project/new", json=test_project)
    res = client.get("/api/v1/project/")
    assert res.json["data"][0]["accounts"][0]["username"] == 'john123'
    assert res.json["data"][0]["accounts"][1]["username"] == 'sam69'

def test_get_people(client,db_conn):
   
    q1 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('john','mark','john123','321')"""
    q2 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('sam','johnstone','sam69','123')"""
    q3 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('Taka','Minamino','taka12','690')"""
    with db_conn as conn: 
        conn.execute(q1)
        conn.execute(q2)
        conn.execute(q3)
    res = client.get("/api/v1/project/allPeople")
    assert res.json["data"][1]["username"] == 'john123'
    assert res.json["data"][2]["username"] == 'sam69'
    assert res.json["data"][3]["username"] == 'taka12'

    assert res.json["data"][1]["lastName"] == 'mark'
    assert res.json["data"][2]["lastName"] == 'johnstone'
    assert res.json["data"][3]["lastName"] == 'Minamino'

    assert res.json["data"][1]["firstName"] == 'john'
    assert res.json["data"][2]["firstName"] == 'sam'
    assert res.json["data"][3]["firstName"] == 'Taka'