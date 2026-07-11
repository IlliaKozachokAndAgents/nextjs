import logging
from typing import Annotated

from pwdlib import PasswordHash

from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, Depends, HTTPException, status, Response

from models import AuthSession
from crud import UserCRUD, AuthSessionCRUD

logger = logging.getLogger(__name__)
router = APIRouter(tags=['Authorization'])


class AuthorizationResponse(BaseModel):
    massage: str


password_hash = PasswordHash.recommended()


@router.post('/authorize', response_model=AuthorizationResponse)
def authorize(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with UserCRUD() as user_crud:
        try:
            user = user_crud.get_by_email(form_data.username)
            if password_hash.verify(form_data.password, user.password):
                with AuthSessionCRUD() as auth_session_crud:
                    auth_session = auth_session_crud.create(
                        AuthSession(user_uid=user.uid)
                    )
                response.set_cookie('session_id', auth_session.str_uid, httponly=True) # secure = True
                return AuthorizationResponse(massage='Successfully authorized!')
        except Exception as err:
            logger.exception(err)
            password_hash.verify(
                form_data.password, password_hash.hash('Time placeholder')
            )

    raise HTTPException(
        headers={'WWW-Authenticate': 'Bearer'},
        detail='Could not validate credentials',
        status_code=status.HTTP_401_UNAUTHORIZED,
    )

@router.delete('/logout', response_model=AuthorizationResponse)
def logout(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with UserCRUD() as user_crud:
        try:
            user = user_crud.get_by_email(form_data.username)
            if password_hash.verify(form_data.password, user.password):
                with AuthSessionCRUD() as auth_session_crud:
                    auth_session = auth_session_crud.create(
                        AuthSession(user_uid=user.uid)
                    )
                response.set_cookie('session_id', auth_session.str_uid)
                return AuthorizationResponse(massage='Successfully authorized!')
        except Exception as err:
            logger.exception(err)
            password_hash.verify(
                form_data.password, password_hash.hash('Time placeholder')
            )

    raise HTTPException(
        headers={'WWW-Authenticate': 'Bearer'},
        detail='Could not validate credentials',
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
