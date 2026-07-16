from app.schemes.phone import PhoneReadToOrder

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class PlaceOrderItemRead(BaseModel):
    """
    Схема которая формирует данные для другой схемы которая формирует ответ для эндпоинта place order
    """
    
    model_config = ConfigDict(from_attributes=True)
    phone_quantity: int
    ordered_at: datetime
    ordered_phone: PhoneReadToOrder = Field(alias='phone', serialization_alias='ordered_phone')


class PlaceOrderRead(BaseModel):
    """Схема которая формирует ответ для эндпоинта place order. 
    Нужна чтобы пользователь увидел id заказа и какой заказ он делает"""

    model_config = ConfigDict(from_attributes=True)

    order_id: int = Field(alias='id', serialization_alias='order_id')
    total_cost: int
    status: str
    address: str

    your_ordered_phones: list[PlaceOrderItemRead] = Field(alias='order_items', serialization_alias='your_ordered_phones')


class UserOrdersRead(BaseModel):
    """
    Схема которая формирует ответ для эндпоинта получения списка своих заказов
    """
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(alias='id', serialization_alias='your_id')
    username: str

    orders: list[PlaceOrderRead] = Field(alias='orders', serialization_alias='your_orders')