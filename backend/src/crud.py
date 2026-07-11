from uuid import UUID

from sqlmodel import create_engine, Session, select

from config import POSTGRES_URL
from models import User, AuthSession


class ObjectNotFound(Exception):
    pass


class BaseCRUD:
    def __init__(self) -> None:
        engine = create_engine(POSTGRES_URL, echo=True)
        self.session = Session(engine)

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        self.session.close()


class UserCRUD(BaseCRUD):
    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_email(self, email: str) -> User:
        return self.session.exec(select(User).where(User.email == email)).one()

    def get_by_key(self, key: UUID) -> User:
        if user := self.session.get(User, key):
            return user
        raise ObjectNotFound(f'User {key} not found!')


class AuthSessionCRUD(BaseCRUD):
    def create(self, auth_session: AuthSession) -> AuthSession:
        self.session.add(auth_session)
        self.session.commit()
        self.session.refresh(auth_session)
        return auth_session

    def get_by_key(self, key: UUID | str) -> AuthSession:
        if auth_session := self.session.get(AuthSession, key):
            return auth_session
        raise ObjectNotFound(f'AuthSession {key} not found!')

    def delete_by_key(self, key: UUID | str) -> AuthSession:
        auth_session = self.get_by_key(key)
        self.session.delete(auth_session)
        self.session.commit()
        return auth_session
    
    def update(self, auth_session: AuthSession) -> AuthSession:
        self.session.add(auth_session)
        self.session.commit()
        self.session.refresh(auth_session)
        return auth_session
