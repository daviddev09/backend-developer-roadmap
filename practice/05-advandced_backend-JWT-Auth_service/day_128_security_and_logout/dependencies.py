import jwt
from models import Base
from fastapi import Depends
from auth import AuthService
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from settings import SECRET_KEY, ALGORITHM, DATABASE_URL, ACCESS_TOKEN_MINUTES, REFRESH_TOKEN_DAYS, CONTEXT

pwd_context = CONTEXT

engine = create_async_engine(url=f'{DATABASE_URL}')
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# -----------get_session_functions---------------

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

async def get_service(session: AsyncSession=Depends(get_db_session)):
    return AuthService(session=session)

# ------------JWT functions------------

async def create_jwt_token(data: dict[str,str], token_time: timedelta):
    to_encode = data.copy()

    exp = datetime.now(timezone.utc) + token_time
    to_encode.update({'exp': exp}) # type: ignore
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

async def creta_access_token(sub: str):
    payload = {
        'sub': sub,
        'type': 'access',
    }
    return await create_jwt_token(data=payload, token_time=timedelta(minutes=ACCESS_TOKEN_MINUTES))

async def create_refresh_token(sub: str):
    payload = {
        'sub': sub,
        'type': 'refresh',
    }
    return await create_jwt_token(data=payload, token_time=timedelta(days=REFRESH_TOKEN_DAYS))

async def decode_jwt_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore

# --------------hashing functions----------------

async def create_password_hash(password: str):
    return pwd_context.hash(password)

async def verify_password(password: str, hashed_password: str):
    
    return pwd_context.verify(password, hashed_password)
