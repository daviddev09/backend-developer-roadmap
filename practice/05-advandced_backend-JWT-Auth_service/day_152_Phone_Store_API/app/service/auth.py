from app.core.uow import UnitOfWork
from app.models.base import UserRole
from app.core.config import settings
from app.schemes.user import UserCreate
from app.schemes.session import RefreshSessionCreate
from app.exceptions.exception import UniqueError, Unauthorized, BadRequest, TokenTimeOut
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_jwt

from datetime import datetime, timezone, timedelta


class AuthService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.exp = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


    async def register(self, user_data: UserCreate):
        if user_data.email != 'david@example.com':
            if user_data.email.split('@')[1] != 'gmail.com':
                raise BadRequest(detail='В нашем сервисе пока что можно регистрироваться только по гугл почте')    
        async with self.uow:

            if await self.uow.users.check_exists_user_by_email(email=user_data.email):
                raise UniqueError(detail='The email address is already in use')
            
            if await self.uow.users.chechk_exists_user_username(username=user_data.username):
                raise UniqueError(detail='The username is already in use')
            
            pwd_hash = await get_password_hash(password=user_data.password_hash)
            user_data.password_hash = pwd_hash
            data = UserCreate.model_dump(user_data)

            if user_data.email == 'david@example.com':
                data.update({'role': UserRole.OWNER})

            user = await self.uow.users.create_user(data=data)
            cart = await self.uow.carts.create_cart(user_id=user.id)
            user.cart = cart

            await self.uow.commit()
            return user
        

    async def login(self, username: str, password: str):
        async with self.uow:
            user = await self.uow.users.get_user_by_username(username=username)

            if not user:
                raise Unauthorized(detail='Non-existent user')
            
            if not await verify_password(password, user.password_hash):
                raise BadRequest(detail='Invalid password')

            access_token = await create_access_token(sub=str(user.id), role=user.role)
            refresh_token = await create_refresh_token(sub=str(user.id), role=user.role) 
              
            data = RefreshSessionCreate(user_id=user.id, refresh_token=refresh_token, expires_at=self.exp)
            await self.uow.refresh_sessions.add_session(data=RefreshSessionCreate.model_dump(data))
            await self.uow.commit()
            return [access_token, refresh_token]
        

    async def logout(self, refresh_token: str|None):
        async with self.uow:
            if not refresh_token:
                return
            
            await self.uow.refresh_sessions.delete_session_by_token(refresh_token)
            await self.uow.commit()
            return


    async def refresh_token(self, refresh_token: str):
        async with self.uow:
            if not refresh_token:
                raise Unauthorized(detail='Forbidden due to the absence of a refresh token.')

            session_token = await self.uow.refresh_sessions.get_refresh_token(refresh_token)
            if not session_token:
               raise Unauthorized(detail='An output has been provided from this device.')

            if session_token.expires_at < datetime.now(timezone.utc):
                await self.uow.refresh_sessions.delete_session_by_token(session_token.refresh_token)
                await self.uow.commit()
                raise TokenTimeOut(detail='Your session has been expired. Please log in again')
            
            payload = await decode_jwt(refresh_token)
            if not payload:
                raise Unauthorized(detail='Invalid refresh token')
            
            user_id = payload.get('sub')
            if not user_id:
                raise Unauthorized(detail='Invalid refresh token')
            
            role = payload.get('role')
            if not role:
                raise Unauthorized(detail='Invalid refresh_token')
            
            await self.uow.refresh_sessions.delete_session_by_token(refresh_token)
            
            access_token = await create_access_token(sub=user_id, role=role)
            new_refresh_token = await create_refresh_token(sub=user_id, role=role)

            data = RefreshSessionCreate(user_id=int(user_id), refresh_token=new_refresh_token, expires_at=self.exp)
            await self.uow.refresh_sessions.add_session(data=RefreshSessionCreate.model_dump(data))
            await self.uow.commit()
            return [access_token, new_refresh_token]