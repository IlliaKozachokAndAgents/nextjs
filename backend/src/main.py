# ##################################################################################
# from typing import Annotated
# from datetime import timedelta, datetime, timezone

# import jwt
# from jwt.exceptions import InvalidTokenError

# from pydantic import BaseModel
# from pwdlib import PasswordHash

# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# class Token(BaseModel):
#     access_type: str
#     access_token: str


# class TokenData(BaseModel):
#     username: str | None = None


# class UserInDB(BaseModel):
#     username: str
#     disabled: bool
#     hashed_password: str


# def get_user(db: dict, username: str):
#     if username in db:
#         return UserInDB(**db[username])


# fake_users_db = {
#     'test@test.com': {
#         'disabled': False,
#         'username': 'test@test.com',
#         'hashed_password': '$argon2id$v=19$m=65536,t=3,p=4$zz6yK3aSO6t38ElHevmGkQ$PpWnyUAfa2+6s+sHgX5FG8WQCumrmEaX8O7ObO453NU'
#     },
#     'test2@test.com': {
#         'disabled': True,
#         'username': 'test2@test.com',
#         'hashed_password': '$argon2id$v=19$m=65536,t=3,p=4$OP/81fjoatDyj8z/u/LKSg$xijWeOAkDOGD8+iIPcDYuYSi9nIDmJzNS2GO77IQ/rQ'
#     }
# }


# JWT_ALGORITHM = "HS256"
# JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
# JWT_SECRET_KEY = "1b0055439cad00e3f0d85e2a9f8baa34f012531a1157f7d68210ffeb160f6aef"

# app = FastAPI()

# # Access Flow
# password_hash = PasswordHash.recommended()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({'exp': expire})
#     encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
#     return encoded_jwt

# def authenticate_user(db: dict, username: str, password: str) -> bool | UserInDB:
#     user = get_user(db, username)
#     if not user:
#         password_hash.verify(
#             password,
#             password_hash.hash('for same check time with existing user')
#         )
#         return False
#     if not password_hash.verify(password, user.hashed_password):
#         return False
#     return user


# @app.post('/token')
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user = authenticate_user(
#         fake_users_db, form_data.username, form_data.password
#     )

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Could not validate credentials',
#             headers={'WWW-Authenticate': 'Bearer'}
#         )
#     access_token_expire = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         {'sub': user.username}, access_token_expire
#     )
#     return Token(access_token=access_token, access_type='bearer')
# # Access Flow

# # Using
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail='Could not validate credentials',
#         headers={'WWW-Authenticate': 'Bearer'}
#     )

#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
#         username = payload.get('sub')
#         if username is None:
#             return credential_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError as err:
#         raise credential_exception from err

#     user = get_user(fake_users_db, token_data.username)
#     if user is None:
#         raise credential_exception
#     return user


# async def get_current_active_user(current_user: Annotated[UserInDB, Depends(get_current_user)]):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail='Inactive user')
#     return current_user


# @app.get('/users/me')
# async def get_me(current_user: Annotated[UserInDB, Depends(get_current_active_user)]):
#     return current_user


# @app.get("/users/me/items")
# async def read_items(current_user: Annotated[UserInDB, Depends(get_current_active_user)]):
#     return [{'item_id': 'foo', 'owner': current_user.username}]
# # End Using Access Flow


# ###################################################################################

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


@app.post('/users', response_model=User)
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
