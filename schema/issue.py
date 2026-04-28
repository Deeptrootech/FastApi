from pydantic import BaseModel

from models.issues import PriorityEnum


class CreateIssue(BaseModel):
    title: str
    description: str
    priority: PriorityEnum
    assigned_to: int


class IssueStatus(BaseModel):
    status: str
