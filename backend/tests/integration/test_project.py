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
VALUES (%(name)s,%(description)s) RETURNING id;""",
                project,
            )
            id = cur.fetchone()[0]
            project["id"] = id
            expected_projects.append(project)
        db_conn.commit()
    res = client.get("/api/v1/project/")
    assert res.status_code == 200
    assert res.json == {"msg": "projects", "data": expected_projects}


def test_projects_list_db_error(client):
    with mock.patch(
        "app.project.routes.get_projects",
        side_effect=Error("Fake error executing query"),
    ) as p:
        res = client.get("/api/v1/project/")

        assert res.status_code == 500
        p.assert_called()
        assert res.json == {
            "error": "Database Error",
            "msg": "Fake error executing query",
        }


def test_project_route(client, db_conn):
    test_project = {
        "name": "Project1",
        "description": "New Project",
        "accounts": "1,2,3"
    }
    q1 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES (john,mark,john123,321)"""
    q2 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES (sam,johnstone,sam69,123)"""
    q3 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES (Taka,Minamino,taka12,690)"""
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
        attribute = cur.fetchone()
        assert attribute["name"] == test_project["name"]
        assert attribute["description"] == test_project["description"]