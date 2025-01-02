from fastapi import APIRouter, Depends, status
from ..utils import crud
from typing import List
from typing_extensions import Annotated  # only if python <= 3.8.... otherwise can import from typing.
from ..schema import users
from sqlalchemy.orm import Session
from ..database import get_db, engine, Base

router = APIRouter(tags=["Users"])

Base.metadata.create_all(bind=engine)


@router.get("/get_users", status_code=status.HTTP_200_OK, response_model=List[users.UserBase])
async def read_users(db: Annotated[Session, Depends(get_db)]):
    db_users = crud.get_all_users(db)
    return db_users
