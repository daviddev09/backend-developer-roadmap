import asyncio

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis # type: ignore
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):

    redis = aioredis.from_url('redis://localhost:6379/0', encoding='utf8', decode_responses=True) # type: ignore

    FastAPICache.init(backend=RedisBackend(redis=redis), prefix='fastapi-cache')
    print('Redis кэш успешно инициализирован!')

    yield

    await redis.aclose() # type: ignore
    

app = FastAPI(lifespan=lifespan)


@app.get('/heavy-computation')
@cache(expire=60)
async def computate():
    print('Подключение к Postgres')
    await asyncio.sleep(2)

    return{
        'message': 'success'
    }