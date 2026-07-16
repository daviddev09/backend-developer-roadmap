from app.core.uow import UnitOfWork
from app.schemes.user import UserUpdate
from app.exceptions.exception import EntityNotFound, BadRequest, UniqueError, AccessDenied
class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def get_user(self, user_id: int):
        async with self.uow:
            user = await self.uow.users.get_user_by_id(user_id=user_id)
            if not user:
                raise EntityNotFound(detail='User not found')
            return user
        
    
    async def change_profile(self, user_id: int, data: UserUpdate):
        async with self.uow:
            user = await self.uow.users.get_user_by_id(user_id)
            if not user:
                raise EntityNotFound(detail='Profile not found, ou might have logged out')
            
            if data.username == user.username:
                raise BadRequest(detail='You is already using this username')
            
            if await self.uow.users.chechk_exists_user_username(data.username):
                raise UniqueError(detail='The username is already in use')
            
            user = await self.uow.users.change_profile(user_id=user_id, new_data=UserUpdate.model_dump(data))
            await self.uow.commit()
            return user
            
    async def delete(self, user_id: int):
        async with self.uow:
            if not await self.uow.users.check_exists_user_by_id(user_id):
                raise EntityNotFound(detail='User not found')
            if await self.uow.users.check_role_user(user_id):
                raise AccessDenied(detail='Owner doesn`t delete the other Owner')

            
            await self.uow.users.delete_user(user_id)
            await self.uow.commit()
            return