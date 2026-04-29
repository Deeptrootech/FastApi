from pydantic import BaseModel


class ListProject(BaseModel):
    id: int
    name: str
    description: str


class CreateProject(BaseModel):
    name: str
    description: str
