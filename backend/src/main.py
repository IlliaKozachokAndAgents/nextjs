from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import create_engine, Session

from models import User
from config import POSTGRES_URL


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


origins = ["http://localhost:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_origins=origins,
    allow_credentials=True,
)


@app.get('/')
async def hello_world():
    return {'data': 'Hello World!'}


@app.post('/users', response_model=User)
async def create_user(user: User) -> User:
    with UserCRUD() as crud:
        return crud.create(user)
