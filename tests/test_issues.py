from tests.utils import (
    create_user,
    get_auth_token,
    create_project,
    create_issue,
    update_issue,
    add_comment,
    add_member
)


def test_create_issue():
    user = create_user("issue@test.com")
    token = get_auth_token(user["email"], user["password"])

    project = create_project(token)
    # Add user as project member before assigning them to an issue
    add_member(project["id"], token, user["id"])
    response = create_issue(token, project["id"], assigned_to=user["id"])
    assert response.status_code == 200


def test_assign_non_member():
    owner = create_user("owner@test.com")
    outsider = create_user("outsider@test.com")

    token = get_auth_token(owner["email"], owner["password"])
    project = create_project(token)

    response = create_issue(
        token,
        project["id"],
        assigned_to=outsider["id"]
    )

    assert response.status_code in [400, 403]


def test_valid_status_transition():
    user = create_user("status@test.com")
    token = get_auth_token(user["email"], user["password"])

    project = create_project(token)
    # Add user as project member before assigning them to an issue
    add_member(project["id"], token, user["id"])
    issue = create_issue(token, project["id"], assigned_to=user["id"]).json()

    response = update_issue(token, issue["id"], "in_progress")

    assert response.status_code == 200


def test_invalid_status_transition():
    user = create_user("status2@test.com")
    token = get_auth_token(user["email"], user["password"])

    project = create_project(token)
    # Add user as project member before assigning them to an issue
    add_member(project["id"], token, user["id"])
    issue = create_issue(token, project["id"], assigned_to=user["id"]).json()

    response = update_issue(token, issue["id"], "INVALID")

    assert response.status_code in [400, 422]


def test_add_comment():
    user = create_user("comment@test.com")
    token = get_auth_token(user["email"], user["password"])

    project = create_project(token)
    # Add user as project member before assigning them to an issue
    add_member(project["id"], token, user["id"])
    issue = create_issue(token, project["id"], assigned_to=user["id"]).json()

    response = add_comment(token, issue["id"], "Test comment")

    assert response.status_code == 200
