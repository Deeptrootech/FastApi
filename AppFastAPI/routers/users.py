from fastapi import APIRouter, Depends, status
from AppFastAPI.utils import crud
from typing import List
from typing_extensions import Annotated  # only if python <= 3.8.... otherwise can import from typing.
from AppFastAPI.schema import users
from sqlalchemy.orm import Session
from AppFastAPI.database import get_db, engine
from AppFastAPI import database

router = APIRouter(tags=["Users"])

database.Base.metadata.create_all(bind=engine)


@router.get("/get_users", status_code=status.HTTP_200_OK, response_model=List[users.UserBase])
async def read_posts(db: Annotated[Session, Depends(get_db)]):
    db_users = crud.get_all_users(db)
    return db_users
