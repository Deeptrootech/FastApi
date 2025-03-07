from sqlalchemy import Column, Integer, String
from database import base, db_engine

class User(base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)

  def __repr__(self):
    return self.name


base.metadata.create_all(db_engine)
