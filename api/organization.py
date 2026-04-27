from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.global_models import Organizations

router = APIRouter()


@router.get("/organizations", response_model=list[Organizations])
def get_organizations(organization_name: str, db: Session = Depends(get_db)):
    org = db.query(Organizations).filter(Organizations.name == organization_name).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

