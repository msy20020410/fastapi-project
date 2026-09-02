"""用户模型。"""
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    full_name: str | None = None

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str