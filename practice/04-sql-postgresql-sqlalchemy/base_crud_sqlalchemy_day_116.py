import asyncio
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


async_engine = create_async_engine(url='sqlite+aiosqlite:///app.db', echo=True)
sync_engine = create_engine(url='sqlite:///app.db')

Base.metadata.drop_all(bind=sync_engine)
Base.metadata.create_all(bind=sync_engine)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

async def create_user():
    async with async_session() as session:

        try:
            user1 = User(name='David')
            user2 = User(name='Ilya')
            user3 = User(name='Alex')

            session.add_all([user1, user2, user3])

            await session.commit()

            await session.refresh(user1)
            print(user1.id)
            
        except Exception as e:
            await session.rollback()
            print(e)
        finally:
            await session.close_all()


async def get_user():
    async with async_session() as session:
        
        try:
            stmt = select(User)

            users = (await session.scalars(stmt)).all()
            for user in users:
                print(user.name)
            return

        except Exception as e:
            await session.rollback()
            print(e)
        finally:
            await session.close_all()


async def main():
    await create_user()
    
    await get_user()

if __name__ == '__main__':
    asyncio.run(main())