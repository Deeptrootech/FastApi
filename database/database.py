from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@database:5432/issue_tracking_db"

# Create Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#  Create a Session Local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Instantiate database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
