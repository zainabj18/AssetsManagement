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


def test_update_project(client, db_conn):
    q1 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('john','mark','john123','321')"""
    q2 = """INSERT INTO accounts(first_name,last_name,username,hashed_password) VALUES ('sam','johnstone','sam69','123')"""
    q3 = """INSERT INTO projects(id,name,description,type) VALUES ('1','project1','newproject1','PUBLIC')"""
    q4 = """INSERT INTO projects(id,name,description,type) VALUES ('2','project2','newproject2','PRIVATE')"""
    with db_conn as conn: 
        conn.execute(q1)
        conn.execute(q2)
        conn.execute(q3)
        conn.execute(q4)

    key = {
        'id': 1,
        'name': 'project1',
        'description': 'newproject1',
        'type': 'PUBLIC',
        'private': True,
        'selectedPeople': [1, 2]
    }

    response = client.post("/api/v1/project/changeProjects", json=key)

    print(response.get_json())

    assert response.status_code == 200

    with db_conn as conn:
        cursor = conn.cursor()
        query = """SELECT * FROM projects WHERE id=%s"""
        cursor.execute(query, (1,))
        result = cursor.fetchone()

        
        column_names = [desc[0] for desc in cursor.description]

       
        result_as_dict = dict(zip(column_names, result))

        assert result_as_dict['name'] == key['name']
        assert result_as_dict['description'] == key['description']
        assert result_as_dict['type'] == key['type']

        query = """SELECT account_id FROM people_in_projects WHERE project_id=%s ORDER BY account_id"""
        cursor.execute(query, (1,))
        results = cursor.fetchall()

       
        results_as_dicts = [dict(zip(column_names, row)) for row in results]

        account_ids = [row['account_id'] for row in results_as_dicts]




# def test_get_project_with_people(client, db_conn):
#     # Add test data to the database
#     q1 = """INSERT INTO accounts(first_name, last_name, username, hashed_password) VALUES ('John', 'Doe', 'johndoe', 'password')"""
#     q2 = """INSERT INTO projects(id, name, description, type) VALUES ('1', 'Project 1', 'Description of project 1', 'PUBLIC')"""
#     q3 = """INSERT INTO people_in_projects(project_id, account_id) VALUES ('1', '1')"""
#     with db_conn as conn: 
#         conn.execute(q1)
#         conn.execute(q2)
#         conn.execute(q3)

#     # Send GET request to /api/v1/project/1
#     response = client.get('/api/v1/project/1')

#     # Check that the response status code is 200 OK
#     assert response.status_code == 200

#     # Check that the response includes the expected project details
#     expected_project_data = {
#         "projectName": "Project 1",
#         "projectDescription": "Description of project 1",
#         "projectType": "PUBLIC",
#         "peopleInProject": [{"firstName": "John", "lastName": "Doe", "username": "johndoe"}]
#     }
#     assert response.json()['data'] == expected_project_data
    