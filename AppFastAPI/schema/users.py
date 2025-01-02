"""
pydantic User model
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Union
from datetime import datetime


# TODO: (Note)
# note that you cannot directly use UploadFile as a field in a Pydantic model,
# because file uploads are handled in multipart/form-data format, which is different from JSON.

# Shared User Schema (Base)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


# Schema for creating a new user (Signup)
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)  # required field


# Schema for returning user information (e.g., in API responses)
class UserResponse(UserBase):
    id: int
    created_at: Union[datetime, None] = None

    class Config:
        orm_mode = True  # allows Pydantic models to work seamlessly with SQLAlchemy models.


# Schema for user login
class UserLogin(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=100)  # required field


# Schema for updating user information
class UserUpdate(BaseModel):
    username: Union[str, None]
    email: Union[str, None]
    password: Union[str, None] = Field(min_length=8, max_length=100)  # required field
