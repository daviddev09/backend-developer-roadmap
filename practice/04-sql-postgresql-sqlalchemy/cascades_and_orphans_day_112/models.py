from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)

    tasks: Mapped[list['Task']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<User {self.name}>'
    

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(default='new')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='tasks')

    def __repr__(self) -> str:
        return f'<Task {self.title}>'