from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_url = 'sqlite:///alchemy.db'

db_engine = create_engine(db_url)

sessionlocal = sessionmaker(bind=db_engine, expire_on_commit=True, autoflush=False, autocommit=False)
session = sessionlocal()

base = declarative_base()
