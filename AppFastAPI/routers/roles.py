from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user, authorized_role
from models.users import Role, User
from schema.role import RoleCreate

router = APIRouter(tags=["Roles"])


@router.get("/roles", dependencies=[Depends(authorized_role(["admin", "user"]))])
def get_roles(db: Annotated[Session, Depends(get_db)]):
    all_roles = db.query(Role).all()
    return all_roles


@router.post("/roles", dependencies=[Depends(authorized_role(["admin"]))])
def create_role(
        role: RoleCreate,
        db: Annotated[Session, Depends(get_db)]
):
    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
