from typing import Annotated

from pwdlib import PasswordHash
from fastapi import APIRouter, status, HTTPException, Depends

from models import User
from crud import UserCRUD
from dependency import validate_session

router = APIRouter(tags=['Users'])

password_hash = PasswordHash.recommended()

@router.post('/user', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User) -> User:
    with UserCRUD() as user_crud:
        def is_user_exist(email):
            try:
                user_crud.get_by_email(email)
                return True
            except:
                return False

        if not is_user_exist(user.email):
            user.password = password_hash.hash(user.password)
            created_user = user_crud.create(user)

            PASSWORD_MASK = '********'
            created_user.password = PASSWORD_MASK
            return created_user

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email already exist!'
        )

@router.get('/me', response_model=User)
async def get_user(user: Annotated[User, Depends(validate_session)]) -> User:
    return user
