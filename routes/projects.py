from fastapi import APIRouter
from fastapi.params import Depends

from dependency import is_authenticated
from schema.project_member import AddProjectMember

router = APIRouter()


@router.get("/projects")
def get_projects(user=Depends(is_authenticated)):
    return {"message": "Projects fetched successfully"}


@router.post("/projects")
def create_project():
    return {"message": "Project created successfully"}


@router.post("/projects/{project_id}/add-member")
def add_project_member(project_id: int, payload: AddProjectMember):
    return {"message": f"{project_id} ---> {payload}"}
