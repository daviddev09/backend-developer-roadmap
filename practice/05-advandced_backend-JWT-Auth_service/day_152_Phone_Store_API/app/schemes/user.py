from app.models.base import UserRole
from app.schemes.cart import CartRead, CartReadForOwner

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(max_length=100)
    email: EmailStr = Field(max_length=255)
    password_hash: str = Field(alias='password')


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(alias='id', serialization_alias='user_id')
    username: str
    email: EmailStr
    role: UserRole
    balance: int
    cart: CartRead


class UserUpdate(BaseModel):
    username: str


class UserCartReadForOwner(BaseModel):
    """
    Схема чтения профиля пользователя с корзиной и товарами, используется когда владелец смотрит профиль пользователя
    """
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int = Field(alias='id', serialization_alias='user_id')
    username: str 
    email: EmailStr
    role: UserRole
    balance: int
    cart: CartReadForOwner