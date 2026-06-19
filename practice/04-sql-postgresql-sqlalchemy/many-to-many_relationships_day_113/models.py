from sqlalchemy import String, Table, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


task_tag_association = Table(
    'task_tag',
    Base.metadata,
    Column('task_id', ForeignKey('tasks.id'), primary_key=True), # type: ignore
    Column('tag_id', ForeignKey('tags.id'), primary_key=True) # type: ignore
)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(15), nullable=False)
    status: Mapped[str] = mapped_column(default='new')

    tags: Mapped[list['Tag']] = relationship(secondary=task_tag_association, back_populates='tasks')

    def __repr__(self) -> str:
        return f'<Task {self.title}>'


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    tasks: Mapped[list['Task']] = relationship(secondary=task_tag_association, back_populates='tags')

    def __repr__(self) -> str:
        return f'<Tag {self.name}>'