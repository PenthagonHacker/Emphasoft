import random
import string
from datetime import datetime, timedelta

import bcrypt
from sqlalchemy.orm import Session

from .database import Token, User
from .schemas import CreateUser, DisplayUser, AuthUser


def hash_password(password: str):
    """Hashing password"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def validate_password(password: str, real_hashed_password):
    """Password validation"""
    return bcrypt.checkpw(password.encode('utf-8'), real_hashed_password)


async def check_user(username: str, db: Session):
    """Checking if user already exists"""
    user = db.query(User).filter(User.username == username).first()
    if user:
        return True


async def get_user_by_username(username: str, db: Session):
    """Get user by username"""
    user = db.query(User).filter(User.username == username).first()
    return user


async def get_user_by_token(token: str, db: Session):
    user = db.query(Token).join(User).filter(Token.token == token).first()
    return user


async def create_token(user_id: int, db: Session):
    """Token generation"""
    letters = string.ascii_lowercase
    token = ''.join(random.choice(letters) for _ in range(25))
    created_token = Token(
        expires=datetime.now() + timedelta(weeks=2),
        user_id=user_id,
        token=token
    )
    db.add(created_token)
    db.commit()
    db.refresh(created_token)
    token = AuthUser.from_orm(created_token)
    return token.token


async def create_user(user: CreateUser, db: Session):
    """Creating new user"""
    hashed_password = hash_password(user.password)
    created_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    user_id = created_user.id
    token = await create_token(user_id, db)
    return {'User': DisplayUser.from_orm(created_user), 'token': token}


async def list_all_users(db: Session):
    """Get list of all users"""
    return db.query(User).all()


async def get_user_by_id(id: int, db: Session):
    """ Get user by id"""
    return db.query(User).filter(User.id == id).first()
