# from sqlalchemy.orm import Session
#
# from .database import get_db
# from . import utils
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='http://127.0.0.1:7777/api-token-auth/')
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     print(token)
#     user = await utils.get_user_by_token(token, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # if not user.is_active:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
#     #     )
#     return user
