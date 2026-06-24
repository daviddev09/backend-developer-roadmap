import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2scheme = OAuth2PasswordBearer(tokenUrl='/login')
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
DB_URL = os.getenv('DATABASE_URL')