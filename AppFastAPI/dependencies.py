from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models.users import User
from auth.jwt import decode_and_verify_jwt_token
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
        ************** CHECKS Is_Authenticated ********************
        Validate the JWT token and retrieve the current user.

        Args:
            token (str): JWT token from the Authorization header.
            db (Session): SQLAlchemy session.

        Returns:
            User: The authenticated user.

        Raises:
            HTTPException: If the token is invalid or the user does not exist.
    """
    payload = decode_and_verify_jwt_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username: str = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def authorized_role(loggedin_user: Annotated[User, Depends(get_current_user)], roles: list[str]):
    if loggedin_user.role not in roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return loggedin_user

# def require_role(required_roles: list[str]):
#     def checker(
#         user: User = Depends(get_current_user),
#         db: Session = Depends(get_db)
#     ):
#         db_user = db.query(User).filter(User.username == user.username).first()
#
#         if not db_user or db_user.role.name not in required_roles:
#             raise HTTPException(status_code=403, detail="Not enough permissions")
#
#         return db_user
#
#     return checker