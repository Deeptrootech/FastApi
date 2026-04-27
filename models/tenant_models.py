from enum import Enum
from sqlalchemy import Column, Integer, String

from database.common_config import Base


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.USER)
