import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from fastapi import FastAPI, Cookie, HTTPException, Response

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

app = FastAPI()

# =====================
# create, decode token
# =====================

async def create_jwt_token(data: dict[str, str|int], token_time: timedelta):

    to_encode = data.copy()
    exp = datetime.now(timezone.utc)+token_time
    to_encode.update({'exp': exp}) # type: ignore
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

async def decode_jwt_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore

async def create_access_token(sub: str, exp_time: timedelta):
    payload: dict[str, str|int] = {
        'sub': sub,
        'type': 'access'
    }
    return await create_jwt_token(payload, exp_time)

async def create_refresh_token(sub: str, exp_time: timedelta):
    payload: dict[str, str|int] = {
        'sub': sub,
        'type': 'refresh'
    }
    return await create_jwt_token(payload, exp_time)

# ====================
#  service functions
# ====================

async def login_function(username: str, email: str):
    if username != 'daviddev' and email != 'david@example.com':
        raise HTTPException(status_code=404, detail='Такого пользователя не существует')
    
    user_id = 1

    access_token = await create_access_token(sub=str(user_id), exp_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) 

    refresh_token = await create_refresh_token(sub=str(user_id), exp_time=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return [access_token, refresh_token]

async def refresh_access_token_function(refresh_token: str|None):
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh_token отсутствует')
    
    try:
        payload = await decode_jwt_token(token=refresh_token)

        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=401, detail='Неверный тип токена')
        
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=401, detail='Невалидный токен')
        
        access_token = await create_access_token(sub=str(user_id), exp_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

        return {
            'access_token': access_token,
            'type': 'bearer'
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token протух')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Refresh token повреждён')

# ==============
#     schemes 
# ==============


class LoginRequest(BaseModel):
    username: str
    email: str


# ================
#    endpoints
# ================

@app.post('/login')
async def login(login_data: LoginRequest, response: Response):
    tokens = await login_function(username=login_data.username, email=login_data.email)

    response.set_cookie(
        key='refresh_token',
        value=tokens[1],
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        'access_token': tokens[0],
        'token_type': 'bearer',
    }

@app.post('/refresh')
async def refresh_access_token(refresh_token: str|None = Cookie(None)):
    return await refresh_access_token_function(refresh_token)