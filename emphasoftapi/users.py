from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

# from .dependencies import get_current_user
from emphasoftapi.schemas import CreateUser, DisplayUser, UpdateUser, AuthUser

from . import utils
from .database import get_db, User

router = APIRouter(prefix='/api/v1/users')
router1 = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api-token-auth/')


@router1.post('/api-token-auth/')
async def auth(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await utils.get_user_by_username(form.username, db)  # type: User
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not utils.validate_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return await utils.create_token(user.id, db)


@router.post('/')
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    if not await utils.check_user(user.username, db):
        db_user = await utils.create_user(user, db)
        return db_user
    raise HTTPException(status_code=400, detail=f'User with that username already exists')


@router.get('/', response_model=List[DisplayUser])
async def list_all_users(db: Session = Depends(get_db)):
    db_user_list = await utils.list_all_users(db)
    return db_user_list


@router.get('/{id}/', response_model=DisplayUser)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    db_user_id = await utils.get_user_by_id(id, db)
    if not db_user_id:
        raise HTTPException(status_code=400, detail=f'User with id {id} doesn\'t exist')
    return db_user_id


# @router.put('/{id}/', response_model=DisplayUser)
# async def update_user_info(id: int, user: UpdateUser, db: Session = Depends((get_db))):
#     if not utils.validate_password(user.password):
#         raise HTTPException(status_code=400, detail='Incorrect current password. Please try again.')


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(token)
    user = await utils.get_user_by_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # if not user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
    #     )
    return user


@router.get("/me", response_model=DisplayUser)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
