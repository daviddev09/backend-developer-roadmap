from app.models.base import Base
from app.models.user import User
from app.models.phone import Phone

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id', ondelete='CASCADE'))
    phone_id: Mapped[int] = mapped_column(ForeignKey('phones.id', ondelete='CASCADE'))
    phone_quantity: Mapped[int]

    cart: Mapped['Cart'] = relationship(back_populates='cart_items')
    phone: Mapped['Phone'] = relationship()



class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    total_cost: Mapped[int] = mapped_column(default=0)


    user: Mapped['User'] = relationship(back_populates='cart')
    cart_items: Mapped[list['CartItem']] = relationship(back_populates='cart', cascade='all, delete-orphan', order_by='CartItem.id')

    phones = association_proxy('cart_items', 'phone')