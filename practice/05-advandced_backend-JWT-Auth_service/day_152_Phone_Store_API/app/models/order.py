from app.models.base import Base
from app.models.user import User
from app.models.phone import Phone

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    phone_id: Mapped[int] = mapped_column(ForeignKey('phones.id'))
    phone_quantity: Mapped[int]
    ordered_at: Mapped[datetime] = mapped_column(default=datetime.now)

    order: Mapped['Order'] = relationship(back_populates='order_items')
    phone: Mapped['Phone'] = relationship()


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    total_cost: Mapped[int]
    status: Mapped[str] = mapped_column(default='pending')
    address: Mapped[str] 
    
    user: Mapped['User'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order', cascade='all, delete-orphan')