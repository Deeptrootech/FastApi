from typing import List
from pydantic import BaseModel


class ListProject(BaseModel):
    id: int
    name: str
    description: str


class ProjectList(BaseModel):
    total: int
    data: List[ListProject]


class CreateProject(BaseModel):
    name: str
    description: str
