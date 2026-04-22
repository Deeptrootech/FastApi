from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models.users import Role, User

router = APIRouter(tags=["Roles"])


@router.get("/roles", dependencies=[Depends(get_current_user)])
def get_roles(db: Annotated[Session, Depends(get_db)]):
    all_roles = db.query(Role).all()
    return all_roles
