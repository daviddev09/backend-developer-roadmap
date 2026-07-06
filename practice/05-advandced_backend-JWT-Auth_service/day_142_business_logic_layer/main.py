import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, status

from repositories.user import UserRepository
from services.user import UserService
from core.database import init_models, get_db_session
from schemas.user import UserCreate, UserRead


app = FastAPI()


async def get_repo(session: AsyncSession = Depends(get_db_session)):
    return UserRepository(session=session)


async def get_service(repo: UserRepository = Depends(get_repo)):
    return UserService(repo=repo)


@app.post('/users', tags=['auth'], response_model=UserRead)
async def register(data: UserCreate, service: UserService = Depends(get_service)):
    user = await service.register_the_user(data=data)
    
    if user == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Этот email занят')
    
    return user


if __name__ == '__main__':
    asyncio.run(init_models())