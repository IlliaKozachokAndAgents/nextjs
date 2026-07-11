from typing import Annotated
from datetime import datetime, timedelta

from fastapi import HTTPException, status, Cookie

from models import User
from crud import UserCRUD, AuthSessionCRUD, ObjectNotFound


def validate_session(session_id: Annotated[str|None, Cookie()] = None) -> User:
    if session_id:
        try:
            with AuthSessionCRUD() as auth_session_crud:
                auth_session = auth_session_crud.get_by_key(session_id)

                if auth_session.updated_at < datetime.now() - timedelta(minutes=15):
                    auth_session_crud.delete_by_key(session_id)
                    raise HTTPException(
                        detail='Could not validate credentials',
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )
                
                if auth_session.created_ad < datetime.now() - timedelta(hours=24):
                    auth_session_crud.delete_by_key(session_id)
                    raise HTTPException(
                        detail='Could not validate credentials',
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )

                try:
                    with UserCRUD() as user_crud:                
                        user = user_crud.get_by_key(auth_session.user_uid)
                except ObjectNotFound:
                    auth_session_crud.delete_by_key(session_id)
                    raise HTTPException(
                        detail='Could not validate credentials',
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )
                
                auth_session.updated_at = datetime.now()
                auth_session_crud.update(auth_session)

                return user

        except Exception:
            pass
    raise HTTPException(
        detail='Could not validate credentials',
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
