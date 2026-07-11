import logging
from typing import Annotated

from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from models import User
from api import auth, users
from dependency import validate_session

logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_origins=origins,
    allow_credentials=True,
)

router = APIRouter()
router.include_router(auth.router, prefix='/auth')
router.include_router(users.router, prefix='/users')

app.include_router(router)

@app.get('/heals-check')
async def hello_world(user: Annotated[User, Depends(validate_session)]):
    return {'data': f'Hello World! Hello {user.email} user!'}
