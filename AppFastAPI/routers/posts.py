from fastapi import Depends, APIRouter, HTTPException, status, Body, Path
from sqlalchemy.orm import Session

from ..database import get_db, engine, Base
from ..schema import posts
from typing_extensions import Annotated
from typing import List

from ..utils import crud

router = APIRouter(tags=["Posts"])  # You can think of APIRouter as a "mini FastAPI" class.

Base.metadata.create_all(bind=engine)


@router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=posts.GetPost)
async def create_post(db: Annotated[Session, Depends(get_db)], post_data: Annotated[posts.CreatePost, Body()]):
    db_post = crud.get_post_by_title(db, post_data.title)
    if db_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="post name already exists.")
    return crud.create_post(db, post_data)


@router.get("/read_posts", status_code=status.HTTP_200_OK, response_model=List[posts.PostBase])
async def read_posts(db: Annotated[Session, Depends(get_db)]):
    db_posts = crud.get_all_post(db)
    return db_posts


@router.get("/read_posts/{post_id}", status_code=status.HTTP_200_OK, response_model=posts.PostBase)
async def read_given_post(post_id: Annotated[int, Path(gt=0)], db: Annotated[Session, Depends(get_db)]):
    retrieved_post = crud.get_post_by_id(db, post_id)
    if not retrieved_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="post Id does not exists.")
    return retrieved_post
