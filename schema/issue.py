from pydantic import BaseModel

from models.issues import PriorityEnum, StatusEnum


class CreateIssue(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    status: StatusEnum
    assigned_to: int


class ResponseIssue(BaseModel):
    id: int
    title: str
    description: str
    priority: PriorityEnum
    status: StatusEnum
    assigned_to_id: int


class ChangeIssueStatus(BaseModel):
    status: str
