from enum import Enum

from sqlalchemy import Column, String, Integer, Enum as AlchemyEnum
from database.database import Base


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    GUEST = "guest"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    user_role = Column(AlchemyEnum(UserRoleEnum, native_enum=False), nullable=False)
