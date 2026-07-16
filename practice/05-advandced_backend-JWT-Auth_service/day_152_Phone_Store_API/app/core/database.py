from app.models.base import Base
from app.core.config import settings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis import asyncio as aioredis


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
redis_client = aioredis.Redis(host='localhost', port=6379, db=1, decode_responses=True)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

