from pydantic import BaseModel


class AddComment(BaseModel):
    text: str
