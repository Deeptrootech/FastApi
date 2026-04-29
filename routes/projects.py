from typing import List

from fastapi import APIRouter, Depends, HTTPException

from database.database import get_db
from dependency import is_authenticated
from models.projects import Project, ProjectMember
from models.users import User
from schema.project import CreateProject, ListProject
from schema.project_member import AddProjectMember, ProjectMemberResponse
from utils.activity_log import create_activity_log

router = APIRouter(dependencies=[Depends(is_authenticated)])


@router.get("/projects", response_model=List[ListProject])
def get_projects(db=Depends(get_db)):
    return db.query(Project).all()


@router.post("/projects")
def create_project(payload: CreateProject, db=Depends(get_db)):
    existing_project = db.query(Project).filter(Project.name == payload.name).first()
    if existing_project:
        raise HTTPException(status_code=400, detail="Project already exists")
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    return {"message": "Project created successfully"}


@router.post("/projects/{project_id}/add-member", response_model=ProjectMemberResponse)
def add_project_member(project_id: int, payload: AddProjectMember, db=Depends(get_db)):
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
