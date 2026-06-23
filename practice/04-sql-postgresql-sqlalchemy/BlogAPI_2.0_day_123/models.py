from datetime import datetime
from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

post_tag_association = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True), # type: ignore
    Column('tag_id', ForeignKey('tags.id'), primary_key=True) # type: ignore
)



class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(100), nullable=False, index=True, unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)

    posts: Mapped[list['Post']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Post(Base):
    __tablename__ = 'posts'

    id:Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='posts')
    tags: Mapped[list['Tag']] = relationship(secondary=post_tag_association, back_populates='posts')



class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    posts: Mapped[list['Post']] = relationship(secondary=post_tag_association, back_populates='tags')
