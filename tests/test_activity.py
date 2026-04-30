from tests.utils import (
    create_user,
    get_auth_token,
    create_project,
    create_issue,
    add_comment,
    get_activities,
    add_member
)


def test_activity_logs():
    user = create_user("activity@test.com")
    token = get_auth_token(user["email"], user["password"])

    project = create_project(token)

    # Add user as project member before assigning them to an issue
    add_member(project["id"], token, user["id"])  # activity log will be created
    issue = create_issue(token, project["id"], assigned_to=user["id"]).json()  # activity log will be created

    add_comment(token, issue["id"], "Activity check")

    response = get_activities(token, issue["id"])

    assert response.status_code == 200
    assert len(response.json()) > 0
