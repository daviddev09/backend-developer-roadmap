import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

DATABASE_URL = os.getenv('DATABASE_URL')

SECRET_KEY = os.getenv('JWT_SECRET_KEY')

ALGORITHM = 'HS256'

ACCESS_TOKEN_MINUTES = 15

REFRESH_TOKEN_DAYS = 7