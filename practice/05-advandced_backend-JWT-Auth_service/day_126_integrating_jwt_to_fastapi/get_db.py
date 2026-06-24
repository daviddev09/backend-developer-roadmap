from sqlalchemy import select
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserRepository:

    def __init__(self, session:AsyncSession) -> None:
        self.session = session

    async def get_user_by_username(self, username: str):
        user = await self.session.execute(select(User).where(User.username == username))

        if user:
            return user.scalar_one_or_none()

    async def get_current_user(self, user_id: int):
        user = await self.session.execute(select(User).where(User.id == user_id))

        if user:
            return user.scalar_one_or_none()
    
    async def create_account(self, username: str, hashed_password: str):

        try:
            user = User(username=username, password_hash=hashed_password)
            self.session.add(user)

            await self.session.commit()
            await self.session.refresh(user)
            return user
        
        except Exception as e:
            await self.session.rollback()
            print(f'Critical error: {e}')