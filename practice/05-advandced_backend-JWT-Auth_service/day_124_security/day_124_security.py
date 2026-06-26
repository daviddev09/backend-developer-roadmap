import os
import asyncio
from dotenv import load_dotenv
from passlib.context import CryptContext

from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

app = FastAPI(title='first day of learning bcrypt')

# ============================
#       Schemas and models
# ============================


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)


# ==============================
#     session and dependencies
# ==============================

engine = create_async_engine(url=f'{os.getenv('DATABASE_URL')}', echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

async def get_password_hash(password: str)-> str:
    
    return pwd_context.hash(password)

async def verify_password(password: str, hashed_password: str)-> bool:

    return pwd_context.verify(password, hashed_password)


# ========================
#           CRUD
# ========================

async def create_user_function(username: str, email: str, password: str, session: AsyncSession):
    try:
        hashed_password = await get_password_hash(password=password)

        user = User(username=username, email=email, password_hash=hashed_password)

        session.add(user)
        
        await session.commit()

        await session.refresh(user)

        return user
    except Exception as e:
        await session.rollback()

        print(f' Failed: {e}')


# =======================
#        endpoints
# =======================
@app.post('/users', response_model=UserRead)
async def create_user(data: UserCreate, session: AsyncSession=Depends(get_db_session)):
    return await create_user_function(username=data.username, email=data.email, password=data.password, session=session)

if __name__ == '__main__':
    asyncio.run(init_models())
    print('Таблицы успешно созданы!')