"""
SQLAlchemy User model
"""
from AppFastAPI.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, DateTime
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    disabled = Column(Boolean, server_default='TRUE')
