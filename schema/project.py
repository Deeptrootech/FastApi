from pydantic import BaseModel


class ListProject(BaseModel):
    id: int
    name: str
    description: str


class ProjectList(BaseModel):
    total: int
    data: list[ListProject]


class CreateProject(BaseModel):
    name: str
    description: str
