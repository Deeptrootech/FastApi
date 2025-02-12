"""
Login/Signup routes
"""
from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from utils.send_mail import send_register_success_email
from pathlib import Path
from logger import logger

from auth.jwt import create_jwt_access_token
from models.users import User
from schema.auth import Token
from schema.users import UserLogin, UserCreate
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


async def validate_and_save_file(file):
    try:
        # Path to save uploaded files inside the 'static/uploads' directory
        UPLOAD_DIR = Path(__file__).parent.parent / "static" / "uploads"
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

        file_size = file.size
        # max size of file is 10 MB
        if file_size > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File size too large. Max size is 10 MB.")

        # File save path
        file_location = UPLOAD_DIR / file.filename

        # Save the file
        content = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        return file_location
    except Exception:
        logger.error("Some Error occured while uploading file")
        return None


@router.post("/signup")
async def signup(
        background_tasks: BackgroundTasks,
        # Handle file upload separately
        file_upload: Annotated[UploadFile, File(description="A file read as UploadFile")],
        db: Session = Depends(get_db),
        # user: UserCreate,
        # (For above) Use the Pydantic model for the user data (Json data) ... If you need to receive data as Form then need to define every field here.. like below
        username: str = Form(...),
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
                    disabled=disabled, file_path=str(uploaded_file_location))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_jwt_access_token({"sub": new_user.username})
    background_tasks.add_task(send_register_success_email, email, username)
    logger.info("SignUp Successfull..!!")
    return {"access_token": access_token, "token_type": "bearer"}
