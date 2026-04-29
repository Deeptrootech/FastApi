from datetime import datetime

from pydantic import BaseModel


class ResponseActivity(BaseModel):
    id: int
    issue_id: int
    action_type: str
    performed_by_id: int
    metadata_: str
    timestamp: datetime

    class Config:
        orm_mode = True
