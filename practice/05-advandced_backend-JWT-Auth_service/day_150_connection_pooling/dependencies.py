import os
from dotenv import load_dotenv

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from models import Base
from service import UserPostService
from repository import UserPostRepository


load_dotenv()
engine = create_async_engine(url=f'{os.getenv('DATABASE_URL')}', echo=False, pool_size=5, max_overflow=10)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

async def get_repo(session: AsyncSession = Depends(get_db_session)):
    return UserPostRepository(session=session)

async def get_service(repo: UserPostRepository = Depends(get_repo)):
    return UserPostService(repo=repo)
