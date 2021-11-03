from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: bool

    class Config:
        orm_mode = True


class User(UserBase):
    id: int


class DisplayUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    is_active: bool
    last_login: str
    is_superuser: bool

    class Config:
        orm_mode = True
