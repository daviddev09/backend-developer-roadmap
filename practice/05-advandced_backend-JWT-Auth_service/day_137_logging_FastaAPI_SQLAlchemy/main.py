import time
import logging
import asyncio

from fastapi import FastAPI, Request, Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import database

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] | %(name)s | %(message)s',
    datefmt= '%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('-----main.py-----')
db_logger = logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@app.middleware('http')
async def logging_middleware(request: Request, call_next ):  # type: ignore
    start_time = time.perf_counter()

    method = request.method
    url = request.url
    
    response = await call_next(request) # type: ignore

    status_code = response.status_code # type: ignore
    process_time = round((time.perf_counter() - start_time) * 1000, 2) 
    
    logging_message = f'Поступил запрос: {method} {url}, выполнился за: {process_time}, статус код: {status_code}'

    if status_code >= 500:
        logger.error(logging_message)
    else:
        logger.info(logging_message)
        
    return response # type: ignore

@app.get('/users')
async def get_users(session: AsyncSession=Depends(database.get_session)):
    users = await session.execute(select(database.User))

    return users.scalars()

@app.post('/users')
async def create_user(username: str, session: AsyncSession=Depends(database.get_session)):
    user = database.User(username=username)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return user

if __name__ == '__main__':
    asyncio.run(database.init_models())
