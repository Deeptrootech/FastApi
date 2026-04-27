from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependency.db_dependencies import get_global_db
from models.global_models import Organizations

router = APIRouter()


@router.get("/organizations")
def get_organizations(organization_name: str, db: Session = Depends(get_global_db)):
    org = db.query(Organizations).filter(Organizations.name == organization_name).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

