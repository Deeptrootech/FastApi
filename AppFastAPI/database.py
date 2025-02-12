"""
Database connection and setup
# https://medium.com/@kevinkoech265/a-guide-to-connecting-postgresql-and-pythons-fast-api-from-installation-to-integration-825f875f9f7d
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: If you change here then also change same in alembic.ini
SQLALCHEMY_DATABASE_URL = "postgresql://deep:1234@localhost:5432/appfastapi_sqlalchemy"
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


# def create_tables():
#     """
#     We had called this function in below commented code (and put that code in the main file).
#     If we wanted to create the database tables while running the FastAPI app...
#
#     Now, we have just 'app = FastAPI()' in main file instead below commented code. (also see use of lifespan for learning)
#     """
#     Base.metadata.create_all(bind=engine)

# from contextlib import asynccontextmanager
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the Database
#     create_tables()
#     yield
#
# app = FastAPI(lifespan=lifespan)  # dependencies=[Depends(get_query_token)]
