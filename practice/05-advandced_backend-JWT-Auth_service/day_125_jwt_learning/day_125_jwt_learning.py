import os
import jwt
import asyncio

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = 'HS256'

async def get_access_token(user_id: int):

    expiration = datetime.now(timezone.utc)+timedelta(minutes=15)

    payload: dict[str, str|datetime] = {
        'sub': str(user_id),
        'exp': expiration,
        'role': 'user'
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

    return access_token

async def verify_access_token(token: str):

    verified_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
    return verified_token

if __name__ == '__main__':

    token = asyncio.run(get_access_token(2))
    print(token)

    print(asyncio.run(verify_access_token(token)))