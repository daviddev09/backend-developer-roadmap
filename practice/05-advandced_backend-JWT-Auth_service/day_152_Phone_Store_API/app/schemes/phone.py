from pydantic import BaseModel, ConfigDict, Field


class PhoneCreate(BaseModel):
    brand: str
    name: str
    storage: str
    price: int
    stock_quantity: int


class FullPhoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone_id: int = Field(alias='id', serialization_alias='phone_id')
    brand: str
    name: str
    storage: str
    price: int
    stock_quantity: int


class PhoneReadWithNoQuantity(BaseModel):
    """
    Схема для чтения телефона без количества в БД, используется когда владелец получает профиль пользователя
    """
    model_config = ConfigDict(from_attributes=True)

    phone_id: int = Field(alias='id', serialization_alias='phone_id')
    brand: str
    name: str
    price: int


class PhoneReadToOrder(BaseModel):
    """
    Схема для формирования данных о телефоне когда пользователь оформляет заказ
    """
    model_config = ConfigDict(from_attributes=True)
    
    brand: str
    name: str
    storage: str
    price: int


class PhoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone_id: int = Field(alias='id', serialization_alias='phone_id')
    name: str
    price: int
    stock_quantity: int


class PhoneUpdate(BaseModel):
    brand: str|None
    name: str|None
    storage: str|None
    price: int|None
    stock_quantity: int|None