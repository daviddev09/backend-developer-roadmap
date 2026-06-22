import crud
import exceptions

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Query, Request

from schemas import UserRead, PostRead, TagRead, UserPostRead, PostUserTagRead, UserCreate, PostCreate, TagCreate

from models import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

app = FastAPI(title='BlogAPI', version='1.0')

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://my-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(exceptions.AppException)
async def app_exception_handler(response: Request, exc: exceptions.AppException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            'status': 'fail',
            'error_type': exc.__class__.__name__,
            'message': exc.detail
        }
    )

sync_engine = create_engine(url='sqlite:///app.db')
async_engine = create_async_engine(url='sqlite+aiosqlite:///app.db')

Base.metadata.drop_all(bind=sync_engine)
Base.metadata.create_all(bind=sync_engine)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session

# ======================================
#             Endpoints
# ======================================

@app.get('/users/{id}', response_model=UserPostRead, tags=['Get endpoints'])
async def get_user_by_id(id:int, session: AsyncSession=Depends(get_session)):
    return await crud.get_user_by_id(user_id=id, session=session)

@app.get('/users', response_model=UserPostRead, tags=['Get endpoints'])
async def get_user_by_username(username: str = Query(description='Введите имя пользователя чтобы получить'), session: AsyncSession=Depends(get_session)):
    return await crud.get_user_by_username(username=username, session=session)

@app.get('/posts/{post_id}', response_model=PostUserTagRead, tags=['Get endpoints'])
async def get_post_by_id(post_id:int, session: AsyncSession = Depends(get_session)):
    return await crud.get_post_by_id(post_id=post_id, session=session)

@app.post('/users', response_model=UserRead, tags=['Create endpoints'])
async def create_user(data: UserCreate, session: AsyncSession=Depends(get_session)):
    return await crud.create_user(username=data.username, email=data.email, session=session)

@app.post('/posts/{user_id}', response_model=PostRead, tags=['Create endpoints'])
async def create_post(text: PostCreate, user_id:int, session: AsyncSession=Depends(get_session)):
    return await crud.create_post(text=text.text, user_id=user_id, session=session)

@app.post('/tags/{post_id}',response_model=TagRead, tags=['Create endpoints'])
async def add_tag(tag_name: TagCreate, post_id: int, session: AsyncSession=Depends(get_session)):
    return await crud.add_tag(tag_name=tag_name.tag_name, post_id=post_id, session=session)