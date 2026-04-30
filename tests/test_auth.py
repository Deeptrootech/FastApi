from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_user(email="test@test.com", password="123456"):
    payload = {
        "name": "Deep",
        "email": email,
        "password": password
    }
    client.post("/auth/register", json=payload)
    return payload


# Register Success
def test_register_success():
    response = client.post("/auth/register", json={
        "name": "Deep",
        "email": "deep@test.com",
        "password": "123456"
    })
    assert response.status_code == 200


# Login Success
def test_login_success():
    user = create_user("login@test.com")

    response = client.post("/auth/login", json={
        "email": user["email"],
        "password": user["password"]
    })

    assert response.status_code == 200
    assert "token" in response.json()


# Login Invalid password
def test_login_wrong_password():
    user = create_user("wrongpass@test.com")

    response = client.post("/auth/login", json={
        "email": user["email"],
        "password": "wrong"
    })

    assert response.status_code == 401
