from app.core.config import settings

import jwt
from fastapi import Response
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_password_hash(password: str):
    return pwd_context.hash(password)

async def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


async def create_jwt(data: dict[str, str], token_time: timedelta):
    to_encode = data.copy()

    exp = datetime.now(timezone.utc) + token_time
    to_encode.update({'exp': exp}) # type: ignore
    return jwt.encode(to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM) # type: ignore

async def decode_jwt(token: str):
    try:
        return jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]) # type: ignore
    except jwt.PyJWTError:
        return None

async def create_access_token(sub: str, role: str):
    payload = {
        'sub': sub,
        'role': role,
        'type': 'access',
    }
    return await create_jwt(data=payload, token_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

async def create_refresh_token(sub: str, role: str):
    payload = {
        'sub': sub,
        'role': role,
        'type': 'refresh',
    }
    return await create_jwt(data=payload, token_time=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

async def set_refresh_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )