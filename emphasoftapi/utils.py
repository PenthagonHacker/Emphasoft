from datetime import datetime, timedelta
import string
import random
import bcrypt
from sqlalchemy.orm import Session

from emphasoftapi.database import User, Token
from emphasoftapi.schemas import CreateUser, DisplayUser


def hash_password(password: str):
    """Hashing password"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


async def create_token(user_id: int):
    """Token generation"""
    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for i in range(25))
    created_token = Token(
        expires=datetime.now() + timedelta(weeks=2),
        user_id=user_id,
        token=token
    )
    return token


async def create_user(user: CreateUser, db: Session):
    """Creating new user"""
    hashed_password = hash_password(user.password)
    created_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = created_user.id
    await create_token(user_id)
    return DisplayUser.from_orm(created_user)
