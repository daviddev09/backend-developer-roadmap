from schemas.user import UserCreate
from core.security import get_password_hash
from repositories.user import UserRepository


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register_the_user(self, data: UserCreate):
        if await self.repo.get_user_by_email(email=data.email):
            return 1
        
        pwd_hash = await get_password_hash(password=data.password)
        user_data = {
            'username': data.username,
            'email': data.email,
            'password_hash': pwd_hash
        }
        return await self.repo.create(data=user_data)
        