from security import get_password_hash, verify_password, get_access_token, decode_access_token
from schemas import UserCreate
from repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo
    
    async def create_user(self, data: UserCreate):
        pwd = await get_password_hash(password=data.password)

        user_data = {
            'username': data.username,
            'email': data.email,
            'password_hash': pwd
        }

        return await self.repo.create_user(data=user_data)
    
    async def login(self, username: str, password: str):
        user = await self.repo.get_user_by_username(username)

        if user:
            if await verify_password(password=password, password_hash=user.password_hash):
                return await get_access_token(user_id=user.id)
            return 1
        return None

    async def get_user_by_id(self, user_id: int):
        return await self.repo.get_user_by_id(user_id=user_id)
    
    async def get_me(self, token: str):
        user_id = await decode_access_token(token)
        if user_id:
            return await self.repo.get_user_by_id(user_id)

