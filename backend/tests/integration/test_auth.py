import os
def test_register_requires_username(client):
    res=client.post("/api/v1/auth/register",json={"password":"user","confirm_password":"user"}
)
    assert res.status_code==400
    assert res.json==[
    {
        "loc": [
            "username"
        ],
        "msg": "field required",
        "type": "value_error.missing"
    }]

def test_register_requires_password(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","confirm_password":"user"}
)
    assert res.status_code==400
    assert res.json==[
    {
        "loc": [
            "password"
        ],
        "msg": "field required",
        "type": "value_error.missing"
    }]

def test_register_requires_confrim_password(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"user"}
)
    assert res.status_code==400
    assert res.json==[
    {
        "loc": [
            "confirmPassword"
        ],
        "msg": "field required",
        "type": "value_error.missing"
    }]

def test_register_requires_password_match(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"user","confirm_password":"u1ser"}
)
    assert res.status_code==400
    assert res.json==[
    {
        "loc": [
            "confirmPassword"
        ],
        "msg": "Passwords do not match",
        "type": "value_error"
    }]

def test_register_requires_password_match(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"user","confirm_password":"u1ser"}
)
    assert res.status_code==400
    assert res.json==[
    {
        "loc": [
            "confirmPassword"
        ],
        "msg": "Passwords do not match",
        "type": "value_error"
    }]

def test_register_accepts_an_account_type(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"user","confirm_password":"user","account_type":"ADMIN"}
)
    assert res.status_code==200

def test_register_accepts_account_privileges(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"user","confirm_password":"user","account_privileges":"PUBLIC"}
)
    assert res.status_code==200

def test_register_enforces_username_unique(client):
    res=client.post("/api/v1/auth/register",json={"username":os.environ["DEFAULT_SUPERUSER_USERNAME"],"password":"user","confirm_password":"user","account_privileges":"PUBLIC"}
)
    assert res.status_code==400
    assert res.json=={"msg":"User already exist with the same username please try a different one."}


def test_register_accepts_aliases(client):
    res=client.post("/api/v1/auth/register",json={"username":"user","password":"user","confirmPassword":"user","accountPrivileges":"PUBLIC","accountType":"VIEWER"}
)
    assert res.status_code==200