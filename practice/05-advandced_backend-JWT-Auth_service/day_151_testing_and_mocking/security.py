import os
import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone



load_dotenv()

oauth2scheme = OAuth2PasswordBearer(tokenUrl='/login')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
ALGORITHM = 'HS256'


async def get_password_hash(password: str):
    return pwd_context.hash(password)

async def verify_password(password: str, password_hash: str):
    return pwd_context.verify(password, password_hash)

async def get_access_token(user_id: int):

    expired = datetime.now(timezone.utc) + timedelta(minutes=15)

    payload: dict[str, datetime|str] = {
        'sub': str(user_id),
        'exp': expired,
        'role': 'user'
    }

    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM) # type: ignore

    return {'access_token': token, 'token_type': 'bearer'}

async def decode_access_token(token: str):
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore

    user_id = (payload.get('sub'))
    if user_id:
        return int(user_id)