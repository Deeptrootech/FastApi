"""
Login/Signup routes
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from AppFastAPI.auth.jwt import create_jwt_access_token
from AppFastAPI.models.users import User
from AppFastAPI.schema.auth import Token
from AppFastAPI.schema.users import UserLogin, UserCreate
from AppFastAPI.database import get_db
from AppFastAPI.utils.hashing import verify_password, hash_password

router = APIRouter()


# user: Annotated[OAuth2PasswordRequestForm, Depends()] ---> to loging with "Authorize" button (with Form input)
# user:  UserLogin ---> to loging with "/login" url (with raw input)
# ******
# POW: Here, we are using "Authorize" button, so that we don't need to pass token everytime into header...
# "Authorize" button will do it by own for every request.
# ******
@router.post("/login", response_model=Token)
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_jwt_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(full_name=user.full_name, username=user.username, email=user.email, hashed_password=hashed_password,
                    disabled=user.disabled)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_jwt_access_token({"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
