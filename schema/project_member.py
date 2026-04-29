from pydantic import BaseModel

from models.projects import RoleEnum


class AddProjectMember(BaseModel):
    user_id: int
    role: RoleEnum


class ProjectMemberResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    role: RoleEnum

    class Config:
        orm_mode = True
