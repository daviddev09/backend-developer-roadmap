from datetime import datetime
from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy


class Base(DeclarativeBase):
    pass


class TaskTag(Base):
    __tablename__ = 'task_tags'

    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), primary_key=True)
    added_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    user: Mapped['User'] = relationship(back_populates='task_tags')
    task: Mapped['Task'] = relationship(back_populates='task_tags')
    tag: Mapped['Tag'] = relationship(back_populates='task_tags')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} {self.__tablename__}'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)

    task_tags: Mapped[list['TaskTag']] = relationship(back_populates='user')

    tasks = association_proxy('task_tags', 'task')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(15), nullable=False)
    status: Mapped[str] = mapped_column(default='new')

    task_tags: Mapped[list['TaskTag']] = relationship(back_populates='task')

    tags = association_proxy('task_tags', 'tag')

    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} {self.title}'
    

class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    task_tags: Mapped[list['TaskTag']] = relationship(back_populates='tag')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} {self.name}'


user = User(name='David', id=1)
tag = Tag(name='SQL')
task = Task(title='Study!!!')

link = TaskTag(tag=tag, added_by_id=user.id)
link.task = task
task.task_tags.append(link)

print(task.tags)