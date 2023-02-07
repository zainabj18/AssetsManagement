from unittest import mock
from psycopg import Error


def test_project_list(client,db_conn):
    expected_projects=[]
    with db_conn.cursor() as cur:
        for x in range(100):
            name=f"Test-{x}"
            project={'name': name,'description': name}
            cur.execute(
        """
    INSERT INTO projects (name,description)
VALUES (%(name)s,%(description)s) RETURNING id;""",
        project,
    )
            id=cur.fetchone()[0]
            project['id']=id
            expected_projects.append(project)
        db_conn.commit()
    res = client.get("/api/v1/project/")
    assert res.status_code == 200
    assert res.json=={"msg": "projects","data":expected_projects}

def test_projects_list_db_error(client):
    with mock.patch(
        "app.project.routes.get_projects", side_effect=Error("Fake error executing query")
    ) as p:
        res = client.get("/api/v1/project/")
        
        assert res.status_code == 500
        p.assert_called()
        assert res.json=={
            "error": "Database Error",
            "msg": "Fake error executing query",
        }