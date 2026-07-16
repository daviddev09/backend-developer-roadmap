from app.schemes.phone import PhoneRead, PhoneReadWithNoQuantity

from pydantic import BaseModel, ConfigDict, Field


class CartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    
class CartItemPhoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone_quantity: int
    phone: PhoneRead


class CartItemReadForOwner(BaseModel):
    """
    Схема чтения телефонов в корзине для владельца, используется для того чтобы смотреть профили пользователей
    """
    model_config = ConfigDict(from_attributes=True)

    phone_quantity: int
    phone: PhoneReadWithNoQuantity


class CartItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cart_id: int = Field(alias='id', serialization_alias='cart_id')
    total_cost: int
    cart_items: list[CartItemPhoneRead]


class CartReadForOwner(BaseModel):
    """
    Схема чтения корзины для владельца, используется чтобы смотреть профиль пользователя
    """
    model_config = ConfigDict(from_attributes=True)


    cart_id: int = Field(alias='id', serialization_alias='cart_id')
    total_cost: int
    cart_items: list[CartItemReadForOwner]