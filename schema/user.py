from pydantic import BaseModel

from models.users import UserRoleEnum


class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    user_role: UserRoleEnum


class LoginUser(BaseModel):
    email: str
    password: str
