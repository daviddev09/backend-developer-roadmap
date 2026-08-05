import redis.asyncio as redis # type: ignore
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True) # type: ignore

    await FastAPILimiter.init(redis_connection) # type: ignore
    
    yield
    
    await redis_connection.close()

app = FastAPI(lifespan=lifespan)

@app.get(
        '/',
        dependencies=[Depends(RateLimiter(times=5, seconds=60))] # type: ignore
)
async def home():
    return {
        'info': 'fastapi_limiter testing'
    }