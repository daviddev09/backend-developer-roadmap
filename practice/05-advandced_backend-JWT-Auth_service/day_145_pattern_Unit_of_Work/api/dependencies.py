from fastapi import Depends

from core.uow import UnitOfWork
from services.user import UserService


async def get_uow():
    return UnitOfWork()


async def get_user_service(uow: UnitOfWork = Depends(get_uow)):
    return UserService(uow=uow)