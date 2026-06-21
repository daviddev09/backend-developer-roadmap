import random
from pydantic import BaseModel, ConfigDict
from fastapi import FastAPI, Depends, Query
from sqlalchemy import select, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ======================
#       ORM models
# ======================


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str]
    status:Mapped[str] = mapped_column(default='new')


# ======================
#    Pydantic schemas
# ======================


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# ===========================================
#      create Table, session, engine and app
# ===========================================

app = FastAPI(title='Task API')

sync_engine = create_engine(url='sqlite:///app.db')
async_engine = create_async_engine(url='sqlite+aiosqlite:///app.db')

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

Base.metadata.drop_all(sync_engine)
Base.metadata.create_all(sync_engine)

async def get_session():
    async with async_session() as session:
        yield session
    


# ======================
#    Create and Read
# ======================

async def create_task(title: str, desc: str, session: AsyncSession):
    statuses = ['new', 'in_progress', 'expired', 'done']
    try:
        
        task = Task(title=title, description=desc, status=random.choice(statuses))

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task
    except Exception as e:
        print(f'Произошла ошибка: {e}')

async def get_tasks(status:str|None, limit: int, offset: int, session: AsyncSession):
    try:
        stmt = select(Task)
        if status:
            stmt =  stmt.where(Task.status == status)            
        stmt = stmt.order_by(Task.id).offset(offset).limit(limit)

        tasks = (await session.scalars(stmt)).all()

        return tasks
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        lst:list[None] = []
        return lst

# ======================
#   FastAPI endpoints
# ======================

@app.post('/tasks', response_model=TaskRead)
async def create_task_endpoint(data: TaskCreate, session: AsyncSession=Depends(get_session)):
    return await create_task(title=data.title, desc=data.description, session=session)

@app.get('/users', response_model=list[TaskRead])
async def get_tasks_endpoint(
    status: str|None = Query(description='Search for status'),
    limit: int = Query(default= 5, ge=1, le=100, description='Количество записей на одной странице'),
    offset: int = Query(default=0, ge=0, description='Пропуск записей'),
    session: AsyncSession = Depends(get_session)
):
    return await get_tasks(status=status, limit=limit, offset=offset, session=session)