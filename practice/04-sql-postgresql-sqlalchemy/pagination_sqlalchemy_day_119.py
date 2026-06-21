import asyncio
from datetime import datetime
from sqlalchemy import func, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

sync_engine = create_engine(url='sqlite:///app.db')
async_engine = create_async_engine(url='sqlite+aiosqlite:///app.db')

class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default='new')
    created_at: Mapped[datetime] = mapped_column(default=func.now())

Base.metadata.drop_all(bind=sync_engine)
Base.metadata.create_all(bind=sync_engine)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def create_tasks():

    print(f'\n-----Running function: {create_tasks.__name__}')
    async with async_session() as session:
        try:

            for n in range(15):
                task = Task(title=f'task{n}', created_at=datetime.now())
                session.add(task)

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f'Exception: {e}')


async def get_tasks_sorted_for_date():

    print(f'\n-----Running function: {get_tasks_sorted_for_date.__name__}')
    async with async_session() as session:

        stmt = select(Task).order_by(Task.created_at.desc())

        tasks = (await session.scalars(stmt)).all()

        for task in tasks:
            print(
                {
                    'task_ID': task.id,
                    'task_title': task.title,
                    'task_status': task.status,
                    'created_time': task.created_at
                }
            )

async def get_paginate_tasks():

    print(f'\n-----Running function: {get_paginate_tasks.__name__}')
    async with async_session() as session:

        page = 1
        limit = 5
        offset = (page - 1) * limit

        stmt = select(Task).order_by(Task.id).offset(offset).limit(limit)

        tasks = (await session.scalars(stmt)).all()

        for task in tasks:
            print(
                {
                    'task_ID': task.id,
                    'task_title': task.title,
                    'task_status': task.status,
                    'created_time': task.created_at
                }
            )

async def get_keyset_paginate_tasks():
    print(f'\n-----Running function: {get_keyset_paginate_tasks.__name__}')
    async with async_session() as session:
        limit= 5
        last_id = 5
        
        stmt = select(Task).where(Task.id > last_id).order_by(Task.id).limit(limit)

        tasks = (await session.scalars(stmt)).all()

        last_id = tasks[-1].id

        for task in tasks:
            print(
                {
                    'task_ID': task.id,
                    'task_title': task.title,
                    'task_status': task.status,
                    'created_time': task.created_at
                }
            )

async def main():

    await create_tasks()

    await get_tasks_sorted_for_date()

    await get_paginate_tasks()

    await get_keyset_paginate_tasks()

if __name__ == '__main__':
    asyncio.run(main())