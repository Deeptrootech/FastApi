from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    action_type = Column(String(100), nullable=False)
    performed_by_id = Column(Integer, ForeignKey("users.id"))
    metadata_ = Column(String(200))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    issue = relationship("Issue", backref="activity_logs")
    performed_by = relationship("User", backref="activity_logs")
