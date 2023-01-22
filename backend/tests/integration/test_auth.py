def test_register_requires_username(client):
    res=client.post("/api/v1/auth/register",json={"username":"user"})
    assert res.status_code==400