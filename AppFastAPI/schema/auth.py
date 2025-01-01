from pydantic import BaseModel
from typing import Union


# Schema for user authentication token
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema for authenticated user data inside token
class TokenData(BaseModel):
    user_id: Union[int, None] = None
    username: Union[str, None] = None
