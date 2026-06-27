from uuid import UUID

from sqlmodel import create_engine, Session, select

from models import User
from config import POSTGRES_URL


class ObjectNotFound(Exception):
    pass


class UserCRUD:
    def __init__(self) -> None:
        engine = create_engine(POSTGRES_URL, echo=True)
        self.session = Session(engine)

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        self.session.close()

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
