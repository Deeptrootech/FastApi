"""
SQLAlchemy User model
"""
from fastapi import UploadFile

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone

from sqlalchemy.orm import relationship

from database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    disabled = Column(Boolean, server_default='TRUE')
    file_path = Column(String, nullable=True)  # Store file path here
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # Actual DB column

    role = relationship("Role")  # Python-side object mapping
