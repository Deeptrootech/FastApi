from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as AlchemyEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from database.database import Base


class RoleEnum(str, Enum):
    OWNER = "owner"
    DEVELOPER = "developer"
    TESTER = "tester"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100))
    created_by_id = Column(Integer, ForeignKey("users.id"))

    created_by = relationship("User", backref="created_projects")


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(AlchemyEnum(RoleEnum, native_enum=False))

    user = relationship("User", backref="project_members")
    project = relationship("Project", backref="project_members")

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="unique_user_project"),
    )
