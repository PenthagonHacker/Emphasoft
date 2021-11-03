from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from . import utils
from emphasoftapi.schemas import CreateUser, DisplayUser

router = APIRouter(prefix='/api/v1/users')


@router.post('/', response_model=DisplayUser)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = await utils.create_user(user, db)
    return db_user

