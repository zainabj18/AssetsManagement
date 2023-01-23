import os
from app.db import get_db,UserRole,DataAccess
from psycopg.rows import dict_row
from werkzeug.security import check_password_hash
from unittest import mock
from psycopg import Error

def test_register_requires_username(client):
    res=client.post("/api/v1/auth/register",json={"password":"fit!xog4?aze08noqLda","confirm_password":"fit!xog4?aze08noqLda"}
)
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "username"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}

def test_register_requires_password(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","confirm_password":"fit!xog4?aze08noqLda"}
)
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}

def test_register_requires_confrim_password(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"fit!xog4?aze08noqLda"}
)
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "confirmPassword"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}

def test_register_requires_password_match(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"fit!xog4?aze08noqLda","confirm_password":"u1ser"}
)
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "confirmPassword"
            ],
            "msg": "Passwords do not match",
            "type": "value_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}

def test_register_accepts_an_account_type(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"fit!xog4?aze08noqLda","confirm_password":"fit!xog4?aze08noqLda","account_type":"ADMIN"}
)
    assert res.status_code==200

def test_register_accepts_account_privileges(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"fit!xog4?aze08noqLda","confirm_password":"fit!xog4?aze08noqLda","account_privileges":"PUBLIC"}
)
    assert res.status_code==200

def test_register_enforces_username_unique(client):
    res=client.post("/api/v1/auth/register",json={"username":os.environ["DEFAULT_SUPERUSER_USERNAME"],"password":"fit!xog4?aze08noqLda","confirm_password":"fit!xog4?aze08noqLda","account_privileges":"PUBLIC"}
)
    assert res.status_code==400
    assert res.json=={"msg":"User already exist with the same username please try a different one.","error":"Username already exist"}


def test_register_accepts_aliases(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"fit!xog4?aze08noqLda","confirmPassword":"fit!xog4?aze08noqLda","accountPrivileges":"PUBLIC","accountType":"VIEWER"}
)
    assert res.status_code==200

def test_register_password_validation_min_length(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"1","confirmPassword":"1","accountPrivileges":"PUBLIC","accountType":"VIEWER"}
)
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg": "password length must be greater than 10",
            "type": "assertion_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}


def test_register_password_validation_max_length(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"tuGlPrutHech0vOzo*lvowaphe2r","confirmPassword":"tuGlPrutHech0vOzo*lvowaphe2r","accountPrivileges":"PUBLIC","accountType":"VIEWER"}
)
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg": "password length must be less than 20",
            "type": "assertion_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}

def test_register_password_validation_mixed_case(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"crahlkap86frasw","confirmPassword":"crahlkap86frasw","accountPrivileges":"PUBLIC","accountType":"VIEWER"})
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg": "password must be mixed case",
            "type": "assertion_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"CRAHLKAP86FRASW","confirmPassword":"CRAHLKAP86FRASW","accountPrivileges":"PUBLIC","accountType":"VIEWER"})
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg": "password must be mixed case",
            "type": "assertion_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}



def test_register_password_validation_letter_and_numbers(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"tHlyUZiRlFoSplx","confirmPassword":"tHlyUZiRlFoSplx","accountPrivileges":"PUBLIC","accountType":"VIEWER"})
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg": "password must be contain letters and numbers",
            "type": "assertion_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"177524253713245","confirmPassword":"177524253713245","accountPrivileges":"PUBLIC","accountType":"VIEWER"})
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg": "password must be contain letters and numbers",
            "type": "assertion_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}

def test_register_password_validation_special_chars(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"chodIpRaf2udrif","confirmPassword":"chodIpRaf2udrif","accountPrivileges":"PUBLIC","accountType":"VIEWER"}
)
    assert res.status_code==400
    assert res.json=={
    "data": [
        {
            "loc": [
                "password"
            ],
            "msg":"password must contain a charecter from ['$', '#', '@', '!', '*']",
            "type": "assertion_error"
        }
    ],
    "error": "Failed to create user from on data provided",
    "msg": "Data provided is invalid"
}

def test_register_password_succes(flask_app,db_conn):
    client=flask_app.test_client()
    username="user"
    password="fit!xog4?aze08noqLda"
    res=client.post("/api/v1/auth/register",json={"username":username,"password":password,"confirmPassword":"fit!xog4?aze08noqLda","accountPrivileges":"PUBLIC","accountType":"VIEWER"})
    assert res.status_code==200
    assert res.json=={"msg":"User registered"}

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""SELECT * FROM accounts WHERE username=%(username)s;""",{"username":"user"})
        user=cur.fetchone()
        assert user['username']=='user'
        assert user['hashed_password']!=password
        assert check_password_hash(user['hashed_password'],password)
        assert user['account_type']==UserRole.VIEWER
        assert user['account_privileges']==DataAccess.PUBLIC
        assert user['first_name']==None
        assert user['last_name']==None

def test_register_db_error(flask_app,db_conn):
    with mock.patch('app.auth.routes.create_user',side_effect=Error("Fake error executing query")) as p:
        client=flask_app.test_client()
        username="user"
        password="fit!xog4?aze08noqLda"
        res=client.post("/api/v1/auth/register",json={"username":username,"password":password,"confirmPassword":"fit!xog4?aze08noqLda","accountPrivileges":"PUBLIC","accountType":"VIEWER"})
        assert res.status_code==500
        assert res.json=={'error': 'Database Connection Error', 'msg': 'Fake error executing query'}
        p.assert_called()
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""SELECT * FROM accounts WHERE username=%(username)s;""",{"username":username})
            user=cur.fetchone()
            assert user==None


def test_login_requires_username_password_comb(client):
    res=client.post("/api/v1/auth/login",json={"password":"fit!xog4?aze08noqLda"}
)
    assert res.status_code==400
    assert res.json=={"msg":"username and password required","error":"Invalid credentials"}

    res=client.post("/api/v1/auth/login",json={"username":"user"}
)
    assert res.status_code==400
    assert res.json=={"msg":"username and password required","error":"Invalid credentials"}

def test_login_check_account_exist(client):
    res=client.post("/api/v1/auth/login",json={"username":"no one","password":"fit!xog4?aze08noqLda"}
)
    assert res.status_code==400
    assert res.json=={"msg":"account doesn't exist","error":"Invalid credentials"}
