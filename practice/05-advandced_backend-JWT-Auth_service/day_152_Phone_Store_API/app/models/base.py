import enum
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserRole(str, enum.Enum):
    USER = 'user'
    OWNER = 'owner'