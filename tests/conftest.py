import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import Base, get_db
from main import app

# **************** Test DB Setup *******************
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ******************* Create tables *******************
Base.metadata.create_all(bind=engine)


# ******************* Override DB dependency *******************
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
