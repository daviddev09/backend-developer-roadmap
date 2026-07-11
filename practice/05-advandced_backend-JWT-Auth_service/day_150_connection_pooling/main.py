import asyncio
from fastapi import FastAPI

from dependencies import init_models
from routers import app_router as router

app = FastAPI()

app.include_router(router)


if __name__ == '__main__':
    asyncio.run(init_models())