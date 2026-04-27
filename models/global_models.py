from sqlalchemy import Column, Integer, String

from database.common_config import Base


class Organizations(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    admin_email = Column(String, nullable=False)
    admin_password = Column(String, nullable=False)
    db_name = Column(String, unique=True)
