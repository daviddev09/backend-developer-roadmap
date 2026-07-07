from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.user import UserService
from core.database import AsyncSessionLocal
from repositories.user import UserRepository


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(session: AsyncSession = Depends(get_db_session)):
    return UserRepository(session=session)


async def get_user_service(repo: UserRepository = Depends(get_user_repo)):
    return UserService(repo=repo)