import jwt
import get_db
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from settings import pwd_context, SECRET_KEY, ALGORITHM


# =======================
# authorization functions
# =======================

async def generate_password_hash(password: str):

    return pwd_context.hash(password)

async def verify_password_hash(pwd: str, pwd_hash: str):

    return pwd_context.verify(pwd, pwd_hash)

async def generate_access_token(user_id: int):

    exp = datetime.now(timezone.utc)+timedelta(minutes=60)

    payload: dict[str, str|datetime] = {
        'sub': str(user_id),
        'exp': exp,
    }

    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM) # type: ignore

    return {'access_token': token, 'token_type': 'bearer'}

async def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore

        user_id = (payload.get('sub'))
        return int(user_id) # type: ignore
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired')

# ==============
#      crud
# ==============
class Userservice:
    def __init__(self, repo: get_db.UserRepository) -> None:
        self.repo = repo

    async def create_user(self, username: str, password: str):
        pwd = await generate_password_hash(password)

        user = await self.repo.create_account(username=username, hashed_password=pwd)

        if user:
            return user
        
        return {
                'status': 'fail',
                'msg': 'Произошла ошибка на стороне БД'
            }


    async def login(self, username: str, password: str):
        user: get_db.User|None = await self.repo.get_user_by_username(username=username)

        if user:

            pwd: str = user.password_hash
            valid_pwd = await verify_password_hash(pwd=password, pwd_hash=pwd)

            if valid_pwd:
                return await generate_access_token(user_id=user.id)
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No Valid password')

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User NotFound')
                
    async def get_user(self, user_id: int):
        user = await self.repo.get_current_user(user_id=user_id)

        if user:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    async def get_current_user(self, token: str):
        user_id = await decode_token(token=token)
        if user_id:
            return await self.repo.get_current_user(user_id=user_id)