import random
import asyncio
from sqlalchemy import ForeignKey, create_engine, select, or_
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

sync_engine = create_engine(url='sqlite:///app.db')
async_engine = create_async_engine(url='sqlite+aiosqlite:///app.db')


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)

    tasks: Mapped[list['Task']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default='new')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='tasks')


Base.metadata.drop_all(bind=sync_engine)

print(f'\n-----Creating The Table-----')
Base.metadata.create_all(bind=sync_engine)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def create_users_and_tasks():
    print(f'\n-----The function works {create_users_and_tasks.__name__}')
    async with async_session() as session:

        try:
            beginnings_of_the_surnames = ['Melnik', 'Atahan', 'Kir']
            endings_of_surnames = ['ov', 'ova']
            status_of_tasks = ['done', 'expired', 'cancelled', 'in_progress', 'new']

            for n in range(15):
                user = User(name=f'user{n}', surname=f'{random.choice(beginnings_of_the_surnames)}{random.choice(endings_of_surnames)}')
                task = Task(title=f'task{n}', status=f'{random.choice(status_of_tasks)}')
                
                user.tasks.append(task)
                session.add_all([user, task])
            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f'An error has occurred: {e}')

async def get_completed_tasks():
    print(f'\n-----The function works {get_completed_tasks.__name__}')
    async with async_session() as session:

        try:
            stmt = select(Task).where(Task.status == 'done')

            tasks = (await session.scalars(stmt)).all()

            for task in tasks:
                print(
                    {
                        'task_ID' : task.id,
                        'task_name' : task.title,
                        'task_status' : task.status
                    }
                )
        except Exception as e:
            print(f'An error has occurred: {e}')

async def get_surnames_ending_with_ov():
    print(f'\n-----The function works {get_surnames_ending_with_ov.__name__}')
    async with async_session() as session:

        try:
            stmt = select(User).where(User.surname.ilike('%ov'))

            users = (await session.scalars(stmt)).all()

            for user in users:
                print(
                    {
                        'user-ID': user.id,
                        'user_name': user.name,
                        'surname': user.surname
                    }
                )
        except Exception as e:
            print(f'An error has occurred: {e}')

async def get_tasks_new_or_in_progress():
    print(f'\n-----The function works {get_tasks_new_or_in_progress.__name__}')
    async with async_session() as session:
        stmt = select(Task).where(or_(Task.status == 'new', Task.status == 'in_progress'))

        tasks = (await session.scalars(stmt)).all()

        for task in tasks:
                print(
                    {
                        'task_ID' : task.id,
                        'task_name' : task.title,
                        'task_status' : task.status
                    }
                )

async def get_tasks_of_user():
    print(f'\n-----The function works {get_tasks_of_user.__name__}')
    async with async_session() as session:
        stmt = select(Task).where(Task.user_id.in_([1, 2, 3]))

        tasks = (await session.scalars(stmt)).all()
        for task in tasks:
                print(
                    {
                        'user_ID' : task.user_id,
                        'task_ID' : task.id,
                        'task_name' : task.title,
                        'task_status' : task.status
                    }
                )

async def main():

    await create_users_and_tasks()

    await get_completed_tasks()

    await get_surnames_ending_with_ov()

    await get_tasks_new_or_in_progress()

    await get_tasks_of_user()

if __name__ == '__main__':
    asyncio.run(main())