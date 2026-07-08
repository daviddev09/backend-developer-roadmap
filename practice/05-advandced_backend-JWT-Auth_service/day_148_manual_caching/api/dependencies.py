from fastapi import Depends

from core.uow import UnitOfWork
from services.user import UserService

import redis.asyncio as aioredis # type: ignore


async def get_uow():
    return UnitOfWork()


async def get_redis():
    redis_client = aioredis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    yield redis_client
    await redis_client.close() # type: ignore


async def get_user_service(uow: UnitOfWork = Depends(get_uow), redis: aioredis.Redis = Depends(get_redis)):
    return UserService(uow=uow, redis=redis)