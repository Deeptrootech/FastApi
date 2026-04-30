from tests.utils import (
    create_user,
    get_auth_token,
    create_project,
    add_member,
    create_issue
)


def test_create_project():
    user = create_user("proj@test.com")
    token = get_auth_token(user["email"], user["password"])

    response = create_project(token)

    assert "id" in response


def test_add_member():
    owner = create_user("owner@test.com")
    member = create_user("member@test.com")

    token = get_auth_token(owner["email"], owner["password"])
    project = create_project(token)

    response = add_member(project["id"], token, member["id"])

    assert response.status_code == 200


def test_non_member_cannot_create_issue():
    owner = create_user("owner2@test.com")
    outsider = create_user("outsider@test.com")

    owner_token = get_auth_token(owner["email"], owner["password"])
    outsider_token = get_auth_token(outsider["email"], outsider["password"])

    project = create_project(owner_token)

    response = create_issue(
        outsider_token,
        project["id"],
        assigned_to=outsider["id"]
    )

    assert response.status_code in [400, 403]
