from sqlalchemy.orm import session
from .models import Post
from .schemas import CreatePost


def get_post_by_id(db: session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    return post


def get_post_by_title(db: session, post_title: str):
    post = db.query(Post).filter(Post.title == post_title).first()
    return post


def get_all_post(db: session, skip: int = 0, limit: int = 100):
    post = db.query(Post).offset(skip).limit(limit).all()
    return post


def create_post(db: session, post: CreatePost):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
