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