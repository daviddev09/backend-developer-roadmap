from redis.asyncio import Redis # type: ignore

from schemas.user import UserCreate, UserRead

from core.uow import UnitOfWork
from core.security import get_password_hash

from exceptions.user import EmailExistsException, UserNotFoundException


class UserService:
    def __init__(self, uow: UnitOfWork, redis: Redis) -> None:
        self.uow = uow
        self.redis = redis

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
        
    async def get_user_by_id(self, id: int):
        async with self.uow:
            
            cache_key = f'user:{id}:profile'

            user_cache =await self.redis.get(cache_key) # type: ignore
            if user_cache:
                return UserRead.model_validate_json(user_cache) # type: ignore
            
            user = await self.uow.users.get_by_id(id)
            if not user:
                raise UserNotFoundException
            
            cache_profile = UserRead.model_validate(user).model_dump_json()
            await self.redis.setex(name=cache_key, time=60, value=cache_profile)
            
            return user