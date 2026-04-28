from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum as AlchemyEnum
from sqlalchemy.orm import relationship
from database.database import Base


class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100))

    priority = Column(AlchemyEnum(PriorityEnum, native_enum=False), nullable=False)
    status = Column(AlchemyEnum(StatusEnum, native_enum=False), nullable=False)

    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    assigned_to = relationship("User", backref="assigned_issues")
