from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    uid: UUID = Field(default_factory=uuid4, primary_key=True)

    email: str
    password: str

    created_ad: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
