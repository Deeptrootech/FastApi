from typing import List

from fastapi import APIRouter, Depends, HTTPException

from database.database import get_db
from dependency import is_authenticated, authorized_role
from models.projects import Project, ProjectMember
from models.users import User
from schema.project import CreateProject, ProjectList, ListProject
from schema.project_member import AddProjectMember, ProjectMemberResponse
from utils.pagination import paginate

router = APIRouter(dependencies=[Depends(is_authenticated)])


@router.get("/projects", response_model=ProjectList)
def get_projects(db=Depends(get_db), limit=10, offset=0):
    project_obj = db.query(Project)
    total, data = paginate(project_obj, offset, limit)
    return {"total": total, "data": data}


@router.post("/projects", response_model=ListProject)
def create_project(payload: CreateProject, db=Depends(get_db),
                   allowed_role=Depends(authorized_role(["admin", "employee"]))):
    """
    Only admin and employee Roles are allowed to access this API
    """
    existing_project = db.query(Project).filter(Project.name == payload.name).first()
    if existing_project:
        raise HTTPException(status_code=400, detail="Project already exists")
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    return project


@router.post("/projects/{project_id}/add-member", response_model=ProjectMemberResponse)
def add_project_member(project_id: int, payload: AddProjectMember, db=Depends(get_db),
                       allowed_role=Depends(authorized_role(["admin", "employee"]))):
    """
    Only admin and employee Roles are allowed to access this API
    """
    # Check project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check user exists
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent duplicate member
    existing = db.query(ProjectMember).filter(
        ProjectMember.user_id == payload.user_id,
        ProjectMember.project_id == project_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already in project")

    # Create member
    projectmember = ProjectMember(
        user_id=payload.user_id,
        project_id=project_id,
        role=payload.role
    )

    db.add(projectmember)
    db.commit()
    db.refresh(projectmember)

    return projectmember


@router.get("/projectsmembers")
def get_project_members(db=Depends(get_db)):
    return db.query(ProjectMember).all()
