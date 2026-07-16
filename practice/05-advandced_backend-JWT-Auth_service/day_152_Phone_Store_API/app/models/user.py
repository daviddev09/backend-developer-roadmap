from app.models.base import Base, UserRole

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    balance: Mapped[int] = mapped_column(default=0)

    token: Mapped['RefreshSession'] = relationship(back_populates='user')
    cart: Mapped['Cart'] = relationship(back_populates='user')
    orders: Mapped[list['Order']] = relationship(back_populates='user')
