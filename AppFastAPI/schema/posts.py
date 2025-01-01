"""
Pydantic schemas for user data
"""
from pydantic import BaseModel
from typing import Union


class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        orm_model = True


class GetPost(PostBase):
    id: Union[int, None]  # int | None

    class Config:
        orm_model = True


class CreatePost(PostBase):
    class Config:
        orm_model = True
