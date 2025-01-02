# FastApi

Here, we have used (Pydantic + SQLAlchemy) model...
```
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

# SQLAlchemy Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

# Pydantic Model
class UserSchema(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
```
But, we also can use (SQLModel) like below... if you don't want to write redundant models (like.. one is for validation and another is for database)
```
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
```
