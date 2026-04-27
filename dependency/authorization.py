from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models.users import User
from auth.jwt import decode_and_verify_jwt_token
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ********************* CHECKS Is_Authenticated -----> authentication ************************************
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """
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


# ********************* CHECKS Is_Authorized -----> authentication + authorization ************************************
def authorized_role(roles: list[str]):
    allowed = {r.lower() for r in roles}

    def dependency_checker(user: User = Depends(get_current_user)):
        if not user.role or user.role.name.lower() not in allowed:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You Are Not Authorized TO Access This"
            )
        return user

    return dependency_checker
