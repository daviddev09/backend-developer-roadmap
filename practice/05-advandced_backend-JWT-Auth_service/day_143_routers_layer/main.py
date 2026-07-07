import asyncio
from fastapi import FastAPI

from core.database import init_models
from api.routers.users import router as user_router

app = FastAPI()

app.include_router(user_router)


if __name__ == '__main__':
    asyncio.run(init_models())