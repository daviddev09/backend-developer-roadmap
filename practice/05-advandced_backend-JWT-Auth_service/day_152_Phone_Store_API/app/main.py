from app.exceptions.exception import AppException
from app.core.database import init_models, redis_client
from app.api.routers.user import app_router as user_router
from app.api.routers.auth import app_router as auth_router
from app.api.routers.cart import app_router as cart_router
from app.api.routers.phone import app_router as phone_router
from app.api.routers.order import app_router as order_router

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

origins = [
    'http://localhost:3000',
    'http://localhost:5173'
]

@app.exception_handler(AppException)
async def app_exception_handler(response: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'status': 'fail',
            'error_type': exc.__class__.__name__,
            'detail': exc.detail
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(phone_router)


if __name__ == '__main__':
    asyncio.run(init_models())