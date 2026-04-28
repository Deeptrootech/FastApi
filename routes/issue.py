from fastapi import APIRouter

from schema.issue import CreateIssue

router = APIRouter()


@router.get("/issues/{issue_id}/issues/")
def get_issue_activities(issue_id: int):
    """
    """
    return {"message": f"{issue_id} ---> activities"}


@router.post("/projects/{project_id}/issues/")
def create_issue(project_id: int, payload: CreateIssue):
    """
    - Only project members can create issues.
    - Assigned member must belong to the project.
    - Priority must be one of: low, medium, high.
    """
    return {"message": f"{project_id} ---> {payload}"}


@router.patch("/issues/{issue_id}/status")
def change_issue_status(issue_id: int, status: CreateIssue):
    """
    Allowed transitions:

    open → in_progress
    in_progress → blocked or resolved
    blocked → in_progress
    resolved → closed
    """
    return {"message": f"{issue_id} ---> {status}"}
