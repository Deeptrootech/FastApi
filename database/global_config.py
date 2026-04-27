"""
Database connection and setup
# https://medium.com/@kevinkoech265/a-guide-to-connecting-postgresql-and-pythons-fast-api-from-installation-to-integration-825f875f9f7d
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://deep:1234@localhost:5432/multitenant_global_db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres_username:postgres_password@localhost:5432/mydatabase"

# Create Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#  Create a Session Local class
GlobalDBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

