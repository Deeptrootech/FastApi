# https://medium.com/@kevinkoech265/a-guide-to-connecting-postgresql-and-pythons-fast-api-from-installation-to-integration-825f875f9f7d
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://deep:1234@localhost:5432/sqlalchemy_db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres_username:postgres_password@localhost:5432/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Instantiate database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
