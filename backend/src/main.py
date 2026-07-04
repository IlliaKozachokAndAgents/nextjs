import logging
from typing import Annotated
from datetime import datetime, timezone, timedelta

import jwt
from pwdlib import PasswordHash

from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import User
from crud import UserCRUD
from dependency import validate_bearer_token
from config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY

logger = logging.getLogger(__name__)

app = FastAPI()
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_origins=origins,
    allow_credentials=True,
)


@app.post('/users', response_model=User, status_code=status.HTTP_201_CREATED)
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


class Token(BaseModel):
    access_token: str
    access_type: str = 'Bearer'


@app.post('/token', response_model=Token)
def auth(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with UserCRUD() as user_crud:
        try:
            user = user_crud.get_by_email(form_data.username)
            if password_hash.verify(form_data.password, user.password):
                return Token(access_token=jwt.encode(
                    key=JWT_SECRET_KEY,
                    algorithm=JWT_ALGORITHM,

                    payload={
                        'sub': str(user.uid),

                        'exp': (
                            datetime.now(timezone.utc)
                            + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
                        )
                    },
                ))
        except Exception as err:
            logger.exception(err)
            password_hash.verify(form_data.password, password_hash.hash('Time placeholder'))
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

@app.get('/heals-check')
async def hello_world(user: Annotated[User, Depends(validate_bearer_token)]):
    return {'data': f'Hello World! Hello {user.email} user!'}
