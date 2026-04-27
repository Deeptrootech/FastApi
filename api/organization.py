from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependency.database import get_global_db
from models.global_models import Organizations

router = APIRouter()


# 1st point (MOST IMP)
# create a Dynamic DB of that organization with the admin user
# 1. create database of given name & bind its session
# 2. apply alembic migrations and create tables.
# 3. create user in that database as an admin user.
# 4. close that db connection and establish with global and create same user as an amin role.
def get_organizations():
    pass


# 2nd point
@router.get("/organizations")
def get_organizations(organization_name: str, db: Session = Depends(get_global_db)):
    org = db.query(Organizations).filter(Organizations.name == organization_name).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
