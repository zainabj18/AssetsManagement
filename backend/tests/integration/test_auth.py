import os
from datetime import datetime, timedelta
from unittest import mock

import jwt
import pytest
from psycopg import Error
from psycopg.rows import dict_row
from werkzeug.security import check_password_hash

from app.db import DataAccess, UserRole, get_db


def test_register_requires_username(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "password": "fit!xog4?aze08noqLda",
            "confirm_password": "fit!xog4?aze08noqLda",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["username"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_requires_password(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"username": "user", "confirm_password": "fit!xog4?aze08noqLda"},
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_requires_confrim_password(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"username": "user", "password": "fit!xog4?aze08noqLda"},
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["confirmPassword"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_requires_password_match(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "fit!xog4?aze08noqLda",
            "confirm_password": "u1ser",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["confirmPassword"],
                "msg": "Passwords do not match",
                "type": "value_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_accepts_an_account_type(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "fit!xog4?aze08noqLda",
            "confirm_password": "fit!xog4?aze08noqLda",
            "account_type": "ADMIN",
        },
    )
    assert res.status_code == 201


def test_register_accepts_account_privileges(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "fit!xog4?aze08noqLda",
            "confirm_password": "fit!xog4?aze08noqLda",
            "account_privileges": "PUBLIC",
        },
    )
    assert res.status_code == 201


def test_register_enforces_username_unique(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": os.environ["DEFAULT_SUPERUSER_USERNAME"],
            "password": "fit!xog4?aze08noqLda",
            "confirm_password": "fit!xog4?aze08noqLda",
            "account_privileges": "PUBLIC",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "msg": "User already exist with the same username please try a different one.",
        "error": "Username already exist",
    }


def test_register_accepts_aliases(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "fit!xog4?aze08noqLda",
            "confirmPassword": "fit!xog4?aze08noqLda",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 201


def test_register_password_validation_min_length(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "1",
            "confirmPassword": "1",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "password length must be greater than 10",
                "type": "assertion_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_password_validation_max_length(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "tuGlPrutHech0vOzo*lvowaphe2r",
            "confirmPassword": "tuGlPrutHech0vOzo*lvowaphe2r",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "password length must be less than 20",
                "type": "assertion_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_password_validation_mixed_case(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "crahlkap86frasw",
            "confirmPassword": "crahlkap86frasw",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "password must be mixed case",
                "type": "assertion_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "CRAHLKAP86FRASW",
            "confirmPassword": "CRAHLKAP86FRASW",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "password must be mixed case",
                "type": "assertion_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_password_validation_letter_and_numbers(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "tHlyUZiRlFoSplx",
            "confirmPassword": "tHlyUZiRlFoSplx",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "password must be contain letters and numbers",
                "type": "assertion_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "177524253713245",
            "confirmPassword": "177524253713245",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "password must be contain letters and numbers",
                "type": "assertion_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_password_validation_special_chars(client):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": "user",
            "password": "chodIpRaf2udrif",
            "confirmPassword": "chodIpRaf2udrif",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 400
    assert res.json == {
        "data": [
            {
                "loc": ["password"],
                "msg": "password must contain a charecter from ['$', '#', '@', '!', '*', '&']",
                "type": "assertion_error",
            }
        ],
        "error": "Failed to create user from on data provided",
        "msg": "Data provided is invalid",
    }


def test_register_password_succes(flask_app, db_conn):
    client = flask_app.test_client()
    username = "user"
    password = "fit!xog4?aze08noqLda"
    res = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "password": password,
            "confirmPassword": "fit!xog4?aze08noqLda",
            "accountPrivileges": "PUBLIC",
            "accountType": "VIEWER",
        },
    )
    assert res.status_code == 201
    assert res.json == {"msg": "User registered"}

    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """SELECT * FROM accounts WHERE username=%(username)s;""",
            {"username": "user"},
        )
        user = cur.fetchone()
        assert user["username"] == "user"
        assert user["hashed_password"] != password
        assert check_password_hash(user["hashed_password"], password)
        assert user["account_type"] == UserRole.VIEWER
        assert user["account_privileges"] == DataAccess.PUBLIC
        assert user["first_name"] == None
        assert user["last_name"] == None


def test_register_db_error(flask_app, db_conn):
    with mock.patch(
        "app.auth.routes.create_user", side_effect=Error("Fake error executing query")
    ) as p:
        client = flask_app.test_client()
        username = "user"
        password = "fit!xog4?aze08noqLda"
        res = client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": password,
                "confirmPassword": "fit!xog4?aze08noqLda",
                "accountPrivileges": "PUBLIC",
                "accountType": "VIEWER",
            },
        )
        assert res.status_code == 500
        assert res.json == {
            "error": "Database Connection Error",
            "msg": "Fake error executing query",
        }
        p.assert_called()
        with db_conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT * FROM accounts WHERE username=%(username)s;""",
                {"username": username},
            )
            user = cur.fetchone()
            assert user == None


def test_login_requires_username_password_comb(client):
    res = client.post("/api/v1/auth/login", json={"password": "fit!xog4?aze08noqLda"})
    assert res.status_code == 400
    assert res.json == {
        "msg": "username and password required",
        "error": "Invalid credentials",
    }

    res = client.post("/api/v1/auth/login", json={"username": "user"})
    assert res.status_code == 400
    assert res.json == {
        "msg": "username and password required",
        "error": "Invalid credentials",
    }


def test_login_check_account_exist(client):
    res = client.post(
        "/api/v1/auth/login",
        json={"username": "no one", "password": "fit!xog4?aze08noqLda"},
    )
    assert res.status_code == 401
    assert res.json == {"msg": "account doesn't exist", "error": "Invalid credentials"}


def test_login_check_account_exist_db_error(client):
    with mock.patch(
        "app.auth.routes.get_user", side_effect=Error("Fake error executing query")
    ) as p:
        res = client.post(
            "/api/v1/auth/login",
            json={
                "username": os.environ["DEFAULT_SUPERUSER_USERNAME"],
                "password": os.environ["DEFAULT_SUPERUSER_PASSWORD"],
            },
        )
        assert res.status_code == 500
        assert res.json == {
            "error": "Database Connection Error",
            "msg": "Fake error executing query",
        }
        p.assert_called()


def test_login_invalid_password(client):
    res = client.post(
        "/api/v1/auth/login",
        json={
            "username": os.environ["DEFAULT_SUPERUSER_USERNAME"],
            "password": os.environ["DEFAULT_SUPERUSER_PASSWORD"] + "s",
        },
    )
    assert res.json == {
        "error": "Invalid credentials",
        "msg": "invalid username/password combination",
    }
    assert res.status_code == 401


def test_login(client):
    res = client.post(
        "/api/v1/auth/login",
        json={
            "username": os.environ["DEFAULT_SUPERUSER_USERNAME"],
            "password": os.environ["DEFAULT_SUPERUSER_PASSWORD"],
        },
    )

    assert res.status_code == 201
    assert "token" in res.json
    token = res.json["token"]

    data = jwt.decode(
        token,
        os.environ["SECRET_KEY"],
        algorithms=[client.application.config["JWT_ALGO"]],
    )
    assert data["account_id"] == 1
    assert data["account_type"] == "ADMIN"
    assert data["account_privileges"] == "CONFIDENTIAL"
    assert datetime.utcfromtimestamp(data["exp"]) > datetime.now()


def test_protected_route_no_token(client):
    res = client.get("/api/v1/auth/admin-status")
    assert res.status_code == 401
    assert res.json == {
        "error": "Missing Token",
        "msg": "Please provide a valid token in the header",
    }


def test_protected_route_expired_token(client):
    token = jwt.encode(
        {
            "account_id": 1,
            "account_type": "ADMIN",
            "account_privileges": "CONFIDENTIAL",
            "exp": datetime.utcnow() - timedelta(minutes=30),
        },
        client.application.config["SECRET_KEY"],
        algorithm=client.application.config["JWT_ALGO"],
    )
    res = client.get("/api/v1/auth/admin-status", headers={"x-access-token": token})
    assert res.status_code == 401
    assert res.json == {"error": "Invalid Token", "msg": "Signature has expired"}


@pytest.mark.parametrize(
    "valid_token",
    [{"account_type": UserRole.ADMIN, "account_privileges": DataAccess.CONFIDENTIAL}],
    indirect=True,
)
def test_protected_valid_token(client, valid_token):
    res = client.get(
        "/api/v1/auth/admin-status", headers={"x-access-token": valid_token}
    )
    assert res.status_code == 200
    assert res.json == {
        "msg": f"None You have admin privileges and data access level of {DataAccess.CONFIDENTIAL.value}"
    }


@pytest.mark.parametrize(
    "valid_token,expected_res",
    [
        (
            {
                "account_type": UserRole.ADMIN,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 200, "msg": "You have admin privileges"},
        ),
        (
            {
                "account_type": UserRole.USER,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 401, "msg": "unauthorised"},
        ),
        (
            {
                "account_type": UserRole.VIEWER,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 401, "msg": "unauthorised"},
        ),
    ],
    indirect=True,
)
def test_protected_rbac_admin(client, valid_token, expected_res):
    res = client.get(
        "/api/v1/auth/admin-status", headers={"x-access-token": valid_token}
    )
    assert res.status_code == expected_res["status_code"]
    assert expected_res["msg"] in res.json["msg"]


@pytest.mark.parametrize(
    "valid_token,expected_res",
    [
        (
            {
                "account_type": UserRole.ADMIN,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 200, "msg": "You have user privileges"},
        ),
        (
            {
                "account_type": UserRole.USER,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 200, "msg": "You have user privileges"},
        ),
        (
            {
                "account_type": UserRole.VIEWER,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 401, "msg": "unauthorised"},
        ),
    ],
    indirect=True,
)
def test_protected_rbac_user(client, valid_token, expected_res):
    res = client.get(
        "/api/v1/auth/user-status", headers={"x-access-token": valid_token}
    )
    assert res.status_code == expected_res["status_code"]
    assert expected_res["msg"] in res.json["msg"]


@pytest.mark.parametrize(
    "valid_token,expected_res",
    [
        (
            {
                "account_type": UserRole.ADMIN,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 200, "msg": "You have viewer privileges"},
        ),
        (
            {
                "account_type": UserRole.USER,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 200, "msg": "You have viewer privileges"},
        ),
        (
            {
                "account_type": UserRole.VIEWER,
                "account_privileges": DataAccess.CONFIDENTIAL,
            },
            {"status_code": 200, "msg": "You have viewer privileges"},
        ),
    ],
    indirect=True,
)
def test_protected_rbac_user(client, valid_token, expected_res):
    res = client.get(
        "/api/v1/auth/viewer-status", headers={"x-access-token": valid_token}
    )
    assert res.status_code == expected_res["status_code"]
    assert expected_res["msg"] in res.json["msg"]
