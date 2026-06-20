from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, selectinload

engine = create_engine("sqlite:///app.db", echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user"
    )


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with SessionLocal() as session:
    user1 = User(name="David")
    user2 = User(name="Marko")

    user1.tasks.extend([
        Task(title="Learn SQL"),
        Task(title="Learn SQLAlchemy"),
    ])

    user2.tasks.append(
        Task(title="Write code")
    )

    session.add_all([user1, user2])
    session.commit()


print("\n=== N+1 ===")
with SessionLocal() as session:
    users = session.scalars(select(User)).all()

    for user in users:
        print(user.name)
        for task in user.tasks:
            print("-", task.title)


print("\n=== selectinload ===")
with SessionLocal() as session:
    users = session.scalars(
        select(User).options(
            selectinload(User.tasks)
        )
    ).all()

    for user in users:
        print(user.name)
        for task in user.tasks:
            print("-", task.title)