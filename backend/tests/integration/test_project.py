from psycopg.rows import dict_row
def test_project_route(client,db_conn):
    test_project = {
        "name": "Project1",
        "description": "New Project",
    }
    res = client.post("/api/v1/projects/new", json=test_project)
    assert res.status_code == 200

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM projects WHERE name=%(name)s AND description=%(description)s;""",
            {"name": test_project["name"],
            "description": test_project["description"]}
        )
        attribute = cur.fetchone()
        assert attribute["name"] == test_project["name"]
        assert attribute["description"] == test_project["description"]
