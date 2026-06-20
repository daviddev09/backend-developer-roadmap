import asyncio
from sqlalchemy import create_engine, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

async_engine = create_async_engine(url='sqlite+aiosqlite:///app.db')
sync_engine = create_engine(url='sqlite:///app.db')

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default='new')


Base.metadata.drop_all(bind=sync_engine)
Base.metadata.create_all(bind=sync_engine)

async def create_tasks():

    async with async_session() as session:
        print('\n-----Creating tasks-----')
        try:

            for n in range(11):
                task = Task(title=f'task {n}')
                session.add(task)

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f'Произошла ошибка {e}')
            raise

async def update_task_in_orm():

    async with async_session() as session:
        print(f'\n-----Running function {update_task_in_orm.__name__}-----')

        try:
            query = select(Task).where(Task.id == 2)
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            task.status = 'done'  # type: ignore

            session.add(task)

            await session.commit()

            print(
                {
                    'ID': task.id, # type: ignore
                    'title': task.title, # type: ignore
                    'status': task.status # type: ignore
                }
            )

        except Exception as e:
            await session.rollback()
            print(f' Произошла ошибка: {e}')
            raise

async def update_task_in_db():

    async with async_session() as session:
        print(f'\n-----Running function {update_task_in_db.__name__}-----')
        try:
            query = update(Task).where(Task.status == 'new').values(status='in_progress')

            await session.execute(query)
            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f'Произогла ошибка: {e}')
            raise

async def delete_task_in_orm():
    print(f'\n-----Running function {delete_task_in_orm.__name__}')

    async with async_session() as session:
        
        try:
            task =await session.get(Task, 1)

            await session.delete(task)
            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f'Произошла ошибка: {e}')
            raise

async def get_tasks():
    print(f'\n-----Running function {get_tasks.__name__}')

    async with async_session() as session:

        try:
            query= select(Task)

            tasks = (await session.scalars(query)).all()
            print('\n-----Окончательное состояние задач-----')

            for task in tasks:
                print(
                    {
                        'ID': task.id,
                        'title': task.title,
                        'status': task.status
                    }
                )

        except Exception as e:
            print(f'Произошла ошибка: {e}')

async def main():

    await create_tasks()

    await update_task_in_orm()

    await update_task_in_db()

    await delete_task_in_orm()

    await get_tasks()

if __name__ == '__main__':
    asyncio.run(main())