import os
from dotenv import load_dotenv

from models import Base
from service import UserService
from repository import UserRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

load_dotenv()
engine = create_async_engine(url=f'{os.getenv('DATABASE_URL')}', echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def get_repo(session: AsyncSession = Depends(get_session)):
    return UserRepository(session=session)


async def get_service(repo: UserRepository = Depends(get_repo)):
    return UserService(repo=repo)
