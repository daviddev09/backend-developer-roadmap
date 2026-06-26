import schemes
import dependencies
from models import User, RefreshSession

from typing import Any
from fastapi import HTTPException
from datetime import timedelta, datetime, timezone

from sqlalchemy import select, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.token_exp = datetime.now(timezone.utc)+timedelta(days=dependencies.REFRESH_TOKEN_DAYS)

    async def save_session_to_db(self, user_id: int, token: str, exp: datetime):
        
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()


        if user:
            await self.session.execute(delete(RefreshSession).where(RefreshSession.user_id == user.id))
            refresh_session = RefreshSession(refresh_token=token, user_id=user.id, expires_at = exp)
            
            self.session.add(refresh_session)
            await self.session.commit()

    async def register_a_user(self, username: str, email: str, password: str)-> list[Any]:
        pwd_hash = await dependencies.create_password_hash(password=password)
        
        user = User(username=username, email=email, password_hash=pwd_hash)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        access_token = await dependencies.creta_access_token(str(user.id))
        refresh_token = await dependencies.create_refresh_token(str(user.id))
        await self.save_session_to_db(user_id=user.id, token=refresh_token, exp=self.token_exp)
        
        return[schemes.UserRead.model_validate(user, from_attributes=True), access_token, refresh_token]
    
    async def login_function(self, email: str, password: str)-> list[str]:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            verified_password = await dependencies.verify_password(password, user.password_hash)
            if verified_password:
                access_token = await dependencies.creta_access_token(str(user.id))
                refresh_token = await dependencies.create_refresh_token(str(user.id))
                await self.save_session_to_db(user_id=user.id, token=refresh_token, exp=self.token_exp)
                return [access_token, refresh_token]
            raise HTTPException(status_code=401, detail='Password is wrong')
        raise HTTPException(status_code=404, detail='User_not_found')    

    async def refresh_token(self, token: str|None):
        if token:
            stmt = select(exists().where(RefreshSession.refresh_token == token))
            result = await self.session.execute(stmt)
            result = result.scalar()
            if result:
                payload = await dependencies.decode_jwt_token(token=token)

                user_id = payload.get('sub')
                if user_id:
                    return {
                        'access_token': await dependencies.creta_access_token(user_id),
                        'type': 'bearer'
                    }
            raise HTTPException(status_code=401, detail='Такого токена не существует' )
                
    async def logout_user(self, token: str|None):
        if token:
            payload = await dependencies.decode_jwt_token(token)
            user_id = payload.get('sub')
            if user_id:
                result = await self.session.execute(select(User).where(User.id == int(user_id)))
                user = result.scalar_one_or_none()
                if user:
                    user.is_logouted = True
                    await self.session.execute(delete(RefreshSession).where(RefreshSession.refresh_token == token))
                    await self.session.commit()


    

