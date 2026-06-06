from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

# class NewClass(SQLModel, table=True):
#     description: str
#     uid: UUID = Field(default_factory=lambda: uuid4(), primary_key=True)
#     new_field: str
