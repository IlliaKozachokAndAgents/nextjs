import re
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator


class User(SQLModel, table=True):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)

    password: str
    email: EmailStr

    created_ad: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, password: str):
        MIX_LENGTH = 8

        if len(password) < MIX_LENGTH:
            raise ValueError('The password is smaller than the minimum size.')
        elif re.search('[0-9]', password) is None:
            raise ValueError('The password does not contain any numbers.')
        elif re.search('[A-Z]', password) is None:
            raise ValueError(
                'The password does not contain any capital letters.')
        elif re.search('[a-z]', password) is None:
            raise ValueError(
                'The password does not contain any lowercase letters.')
        elif re.search('[^A-Za-z0-9]', password) is None:
            raise ValueError(
                'The password does not contain any special characters.')

        return password


class AuthSession(SQLModel, table=True):
    uid: UUID = Field(default=uuid4, primary_key=True)

    user_uid: UUID

    created_ad: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @property
    def str_uid(self):
        return str(self.uid)
