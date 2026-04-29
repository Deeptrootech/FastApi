from fastapi import APIRouter, Depends, HTTPException

from database.database import get_db
from dependency import is_authenticated
from models.activity_logs import ActivityLog
from models.issues import Issue, StatusEnum
from models.projects import Project, ProjectMember
from models.users import User
from schema.activity import ResponseActivity
from schema.issue import CreateIssue, ResponseIssue, ChangeIssueStatus
from utils.activity_log import create_activity_log

router = APIRouter()


@router.get("/issues/{issue_id}/activity/", dependencies=[Depends(is_authenticated)],
            response_model=list[ResponseActivity])
def get_issue_activities(issue_id: int, db=Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    activities = db.query(ActivityLog).filter(ActivityLog.issue_id == issue_id).all()
    return activities


@router.post("/projects/{project_id}/issues/", response_model=ResponseIssue)
def create_issue(project_id: int, payload: CreateIssue, db=Depends(get_db), current_user=Depends(is_authenticated)):
    """
    - Only project members can create issues.
    - Assigned member must belong to the project.
    - Priority must be one of: low, medium, high.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    assigned_to = db.query(User).filter(User.id == payload.assigned_to).first()
    if not assigned_to:
        raise HTTPException(status_code=404, detail="Assigned user not found")

    project_member = db.query(ProjectMember).filter(ProjectMember.user_id == assigned_to.id,
                                                    ProjectMember.project_id == project.id).first()
    if not project_member:
        raise HTTPException(status_code=403, detail="Assigned User is not a member of the project")

    project_member = db.query(ProjectMember).filter(ProjectMember.user_id == current_user.id,
                                                    ProjectMember.project_id == project.id).first()
    if not project_member:
        raise HTTPException(status_code=403, detail="You are not a member of the project")

    issue = Issue(title=payload.title, description=payload.description, priority=payload.priority,
                  status=payload.status, assigned_to_id=payload.assigned_to)
    db.add(issue)
    db.commit()
    db.refresh(issue)

    create_activity_log(issue.id, "issue_created", current_user.id,
                        f"Issue {issue.title} created by {current_user.name}")
    return issue


@router.patch("/issues/{issue_id}/status", response_model=ResponseIssue)
def change_issue_status(issue_id: int, rquest_data: ChangeIssueStatus, db=Depends(get_db),
                        current_user=Depends(is_authenticated)):
    """
    Allowed transitions:

    open → in_progress
    in_progress → blocked or resolved
    blocked → in_progress
    resolved → closed
    """
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    allowed_transition = {
        StatusEnum.OPEN: [StatusEnum.IN_PROGRESS],
        StatusEnum.IN_PROGRESS: [StatusEnum.BLOCKED, StatusEnum.RESOLVED],
        StatusEnum.BLOCKED: [StatusEnum.IN_PROGRESS],
        StatusEnum.RESOLVED: [StatusEnum.CLOSED]
    }
    if rquest_data.status not in allowed_transition.get(issue.status, []):
        raise HTTPException(status_code=400, detail="Invalid status transition")

    issue.status = rquest_data.status
    db.add(issue)
    db.commit()
    db.refresh(issue)

    create_activity_log(issue.id, "status_changed", current_user.id,
                        f"status changed from {issue.status} ----> {rquest_data.status} ")
    return issue
