"""
Pydantic schemas for user data
"""
from pydantic import BaseModel
from typing import Union


class PostBase(BaseModel):
    content: str
    title: str
    genre: str

    class Config:
        from_attributes = True


class GetPost(PostBase):
    id: Union[int, None]  # int | None

    class Config:
        from_attributes = True


class CreatePost(PostBase):
    class Config:
        from_attributes = True
