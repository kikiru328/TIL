def test_health_check(client):
    response = client.get("/") # ping: pong
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
