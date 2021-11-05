from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class GetCurrentUser(UserBase):
    id: int

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: bool

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    first_name: str
    last_name: str
    password: str
    new_password: str
    is_active: bool

    class Config:
        orm_mode = True


class DisplayUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    is_active: bool
    last_login: datetime
    is_superuser: bool

    class Config:
        orm_mode = True


class AuthUser(BaseModel):
    id: int
    token: str
    expires: datetime

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    expires: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        orm_mode = True