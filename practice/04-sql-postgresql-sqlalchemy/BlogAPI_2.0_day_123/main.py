import crud
import exceptions

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Query, Request, Body, Path

from schemas import UserRead, UserPostRead, PostUserTagRead, UserCreate, PostCreate, PostUpdate

from models import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

app = FastAPI(title='Blog API', version='2.0', description='An API that simulates post additions. Includes full CRUD.', contact={'github_username':'daviddev09'})

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

# =============
# GET ENDPOINTS
# =============
@app.get('/users/{id}', response_model=UserPostRead, tags=['Users'])
async def get_user_by_id(id:int, session: AsyncSession=Depends(get_session)):
    return await crud.get_user_by_id(user_id=id, session=session)

@app.get('/users', response_model=UserPostRead, tags=['Users'])
async def get_user_by_username(username: str = Query(description='Введите имя пользователя чтобы получить'), session: AsyncSession=Depends(get_session)):
    return await crud.get_user_by_username(username=username, session=session)

@app.get('/posts/{post_id}', response_model=PostUserTagRead, tags=['Posts'])
async def get_post_by_id(post_id:int, session: AsyncSession = Depends(get_session)):
    return await crud.get_post_by_id(post_id=post_id, session=session)

# ==============
# POST ENDPOINTS
# ==============

@app.post('/users', response_model=UserRead, tags=['Users'])
async def create_user(data: UserCreate, session: AsyncSession=Depends(get_session)):
    """Создаёт нового пользователя
    адрес электронной почты и имя
    пользователя должны быть уникальными"""
    return await crud.create_user(username=data.username, email=data.email, session=session)

@app.post('/posts/{user_id}', response_model=PostUserTagRead, tags=['Posts'])
async def create_post(text: PostCreate = Body(...), user_id:int = Path(...), tag_name: str=Query(description='Write and separate each tag with the # symbol.',
    openapi_examples ={'normal': {'summary':'Пример тегов','value':'#daviddev #09 #programming #sql'}}),
    session: AsyncSession=Depends(get_session)):
    """Создаёт новый пост, чтобы создать пост
    вы должны добавить ID существующего пользователя"""
    return await crud.create_post(text=text.text, user_id=user_id, tag_name=tag_name, session=session)

# =============
# PUT ENDPOINTS
# =============

@app.put('/users/{user_id}', response_model=UserPostRead, tags=['Users'])
async def update_user_username(user_id:int, new_username: str = Body(), session: AsyncSession=Depends(get_session)):
    """Обновляет имя полььзователя
    Новое имя пользователя должно
    быть уникальным"""
    return await crud.update_user_username(user_id=user_id, new_username=new_username, session=session)

@app.put('/posts/{post_id}', response_model=PostUserTagRead, tags=['Posts'])
async def update_post_text_or_tag(post_id: int,data: PostUpdate, session: AsyncSession=Depends(get_session)):
    """Обновляет пост, можно обновить теги
    или же можно обновить текст поста"""
    return await crud.update_post(post_id=post_id, new_text=data.new_text, new_tags=data.new_tags, session=session)

# ================
# DELETE ENDPOINTS
# ================

@app.delete('/users', status_code=200, tags=['Users'])
async def delete_user_with_email_or_id(
    user_id: int|None = Query(default=None, description='Удаление по ID'),
    username: str|None = Query(default=None, description='Удаление по имени пользователя'),
    session: AsyncSession=Depends(get_session)
):
    """Удаляет пользователя по имени пользователя
    или же по ID."""
    return await crud.delete_the_user(user_id=user_id, username=username, session=session)

@app.delete('/posts/{post_id}', status_code=200, tags=['Posts'])
async def delete_post(post_id: int, session: AsyncSession=Depends(get_session)):
    """Удаляет пост"""
    return await crud.delete_post(post_id=post_id, session=session)