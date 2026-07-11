from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    posts: Mapped[list['Post']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='posts')