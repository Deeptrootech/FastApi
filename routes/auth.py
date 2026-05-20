import token

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from authentication.jwt_auth import create_jwt_access_token
from database.database import get_db
from models.users import User
from schema.user import RegisterUser, LoginUser
from utils.email_service import EmailService
from utils.hashing import verify_password, get_password_hash

router = APIRouter()


@router.post("/auth/login")
def login(payload: LoginUser, db=Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email")
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token = create_jwt_access_token({"email": payload.email})
    return {"token": access_token}


@router.post("/auth/register")
def register(background_tasks: BackgroundTasks, payload: RegisterUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(payload.password)
    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hashed_password,
        user_role=payload.user_role
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    email_service = EmailService()
    background_tasks.add_task(
        email_service.send_email,
        to=user.email,
        subject="Registration Successful",
        body="You have successfully registered."
    )

    return {
        "message": "Register successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.get("/users")
def list_users(db=Depends(get_db)):
    users = db.query(User).all()
    return users
