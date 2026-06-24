import service
import asyncio
from settings import DB_URL, oauth2scheme

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from get_db import Base, UserRepository, UserCreate, UserRead
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

app = FastAPI()

engine = create_async_engine(url=f'{DB_URL}')
AsyncSesionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_model():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with AsyncSesionLocal() as session:
        yield session

async def get_repo(session: AsyncSession = Depends(get_session)):
    return UserRepository(session=session)

async def get_service(repo: UserRepository = Depends(get_repo)):
    return service.Userservice(repo=repo)

@app.post('/create-account', response_model=UserRead)
async def create_account(data: UserCreate, service: service.Userservice = Depends(get_service)):
    return await service.create_user(username=data.username, password=data.password)

@app.post('/login')
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), service: service.Userservice = Depends(get_service)):
    return await service.login(username=form_data.username, password=form_data.password)

@app.get('/users/me', response_model=UserRead)
async def get_me(token: str = Depends(oauth2scheme), service: service.Userservice = Depends(get_service)):
    return await service.get_current_user(token)

if __name__ == '__main__':
    asyncio.run(init_model())