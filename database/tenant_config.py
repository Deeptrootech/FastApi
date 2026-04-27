from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_CACHE = {}


def get_db_session(db_name: str):
    if db_name not in DB_CACHE:
        engine = create_engine(
            f"postgresql://deep:1234@localhost:5432/{db_name}"
        )
        TenantDBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        DB_CACHE[db_name] = TenantDBSession

    return DB_CACHE[db_name]  # returns DB session factory (class/function) created by sessionmaker

