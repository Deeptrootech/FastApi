from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_user(email="test@test.com", password="123456"):
    payload = {
        "name": "Test User",
        "email": email,
        "password": password
    }
    response = client.post("/auth/register", json=payload)
    if response.status_code == 200:
        # Extract user ID from registration response
        user_data = response.json().get("user", {})
        payload["id"] = user_data.get("id")
    return payload


def get_auth_token(email, password):
    response = client.post("/auth/login", json={
        "email": email,
        "password": password
    })
    return response.json()["token"]


def get_auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def create_project(token, name="Test Project"):
    response = client.post(
        "/projects/",
        json={
            "name": name,
            "description": "test description"
        },
        headers=get_auth_headers(token)
    )
    return response.json()


def add_member(project_id, token, user_id, role="developer"):
    return client.post(
        f"/projects/{project_id}/add-member",
        json={"user_id": user_id, "role": role},
        headers=get_auth_headers(token)
    )


def create_issue(token, project_id, title="Test Issue", description="Test Description", priority="medium", status="open", assigned_to=None):
    payload = {
        "title": title,
        "description": description,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to or 1  # Default to user ID 1 if not provided
    }
    return client.post(
        f"/projects/{project_id}/issues/",
        json=payload,
        headers=get_auth_headers(token)
    )


def update_issue(token, issue_id, status):
    return client.patch(
        f"/issues/{issue_id}/status",
        json={"status": status},
        headers=get_auth_headers(token)
    )


def add_comment(token, issue_id, text):
    return client.post(
        f"/issues/{issue_id}/comments",
        json={"text": text},
        headers=get_auth_headers(token)
    )


def get_activities(token, issue_id=None):
    if issue_id:
        return client.get(
            f"/issues/{issue_id}/activity/",
            headers=get_auth_headers(token)
        )
    else:
        return client.get(
            "/issues",
            headers=get_auth_headers(token)
        )
