"""
Define JWT utilities here.
"""
import jwt
from typing import Union
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# to get a string like this run: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
REFRESH_SECRET_KEY = "385a608a787dfa2b43490a52661420447d85232704f81eab1358103bc3b4f019"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def create_jwt_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Create a JWT access token.

    params:
        data: The payload to include in the token.
        expires_delta: Expiration time for the token.
    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_and_verify_jwt_token(token: str):
    """
    Decodes and verifies the token, returning the payload if valid.
    Decode and validate a JWT token.

    params:
        token (str): Encoded JWT token.
    Returns:
        dict or None: Decoded payload if valid, otherwise None.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        return decoded_token
    except jwt.PyJWTError:
        return None

