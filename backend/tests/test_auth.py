import json

def test_login_success(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "correctpassword"
    })
    assert response.status_code == 200


def test_login_invalid_password(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_missing_fields(client):
    response = client.post("/auth/login", json={})
    assert response.status_code == 400