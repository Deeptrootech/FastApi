"""
Login/Signup routes
"""
from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from routers.utils import validate_and_save_file
from utils.send_mail import send_register_success_email
from logger import logger

from auth.jwt import create_jwt_access_token
from models.users import User
from schema.auth import Token
from database import get_db
from utils.hashing import verify_password, hash_password

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
    logger.info("Login Successfull..!!")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup")
async def signup(
        background_tasks: BackgroundTasks,

        # Handle file upload separately
        file_upload: Annotated[UploadFile, File(description="A file read as UploadFile")],

        # Dependency Injection
        db: Session = Depends(get_db),

        # user: UserCreate, # Use the Pydantic model for the user data (JSON data)...
        # But, If you need to receive data as Form then need to define every field here... like below
        username: str = Form(...),
        role_id: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        password: str = Form(...),
        disabled: bool = Form(...),
):
    # file upload store
    uploaded_file_location = await validate_and_save_file(file_upload)

    # metadata (data otherthen file upload) store
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(password)
    new_user = User(full_name=full_name, username=username, email=email, hashed_password=hashed_password,
                    disabled=disabled, file_path=str(uploaded_file_location), role_id=role_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_jwt_access_token({"sub": new_user.username})
    background_tasks.add_task(send_register_success_email, email, username)
    logger.info("SignUp Successfull..!!")
    return {"access_token": access_token, "token_type": "bearer"}
