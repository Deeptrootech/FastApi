from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from authentication.jwt_auth import decode_and_verify_jwt_token
from database.database import get_db
from models.users import User
from sqlalchemy.orm import Session

bearer_token_scheme = HTTPBearer()  # get token from header


# ********************* CHECKS Is_Authenticated -----> authentication ************************************
async def is_authenticated(token=Depends(bearer_token_scheme), db: Session = Depends(get_db)):
    """
        Validate the JWT token and retrieve the current user.

        Args:
            token: JWT token from the Authorization header.
            db (Session): SQLAlchemy session.

        Returns:
            User: The authenticated user.

        Raises:
            HTTPException: If the token is invalid or the user does not exist.
    """
    payload = decode_and_verify_jwt_token(token.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email: str = payload.get("email")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


# ********************* CHECKS Is_Authorized -----> authentication + authorization ************************************
def authorized_role(roles: List[str]):
    allowed = {r.lower() for r in roles}

    def dependency_checker(user: User = Depends(is_authenticated)):
        if not user.user_role or user.user_role.lower() not in allowed:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You Are Not Authorized TO Access This API"
            )
        return user

    return dependency_checker
