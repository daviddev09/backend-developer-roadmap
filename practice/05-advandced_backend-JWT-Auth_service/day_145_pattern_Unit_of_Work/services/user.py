from schemas.user import UserCreate

from core.uow import UnitOfWork
from core.security import get_password_hash

from exceptions.user import EmailExistsException


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def register_the_user(self, data: UserCreate):
        async with self.uow:
            if await self.uow.users.get_user_by_email(email=data.email):
                raise EmailExistsException
        
            pwd_hash = await get_password_hash(password=data.password)
            user_data = {
                'username': data.username,
                'email': data.email,
                'password_hash': pwd_hash
            }
            user = await self.uow.users.create(data=user_data)
            await self.uow.commit()
            
            return user
        