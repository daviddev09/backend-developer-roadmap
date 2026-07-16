from app.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column


class Phone(Base):
    __tablename__ = 'phones'

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    storage: Mapped[str]
    price: Mapped[int]
    stock_quantity: Mapped[int]