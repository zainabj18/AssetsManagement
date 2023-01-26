# Test for the path to the type adder
def test_typeAdder_route(client):
    res = client.get("/api/v1/type/adder")
    assert res.status_code == 200
