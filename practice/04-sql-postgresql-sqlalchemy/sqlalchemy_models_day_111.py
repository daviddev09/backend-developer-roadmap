from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

DATABASE_URL = 'sqlite:///:memory:'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(22), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    tasks: Mapped[list['Task']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(default='new')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='tasks')

    def __repr__(self) -> str:
        return f'<Task {self.title}>'


def main():
    print('-----Создание таблиц-----')
    Base.metadata.create_all(bind=engine)

    session=SessionLocal()

    try:
        print('\n --- Шаг 1: Создание пользователя ---')
        new_user = User(username='Daviddev', email='david@example.com')

        print('\n --- Шаг 2: Добавление 3 задач через append() ---')
        task1 = Task(title='Изучить SQL', description='Основы DDL и DML')
        task2 = Task(title='Изучить SQLAlchemy ORM', description='Работа с моделями')
        task3 = Task(title='Оптимизировать БД', description='Индексы и транзакции')

        new_user.tasks.append(task1)
        new_user.tasks.append(task2)
        new_user.tasks.append(task3)

        session.add(new_user)

        print('\n --- Шаг 3: Сохранение данных одной транзакцией (commit) ---')

        session.commit()
        print('Данные успешно сохранены')

        print('\n --- Шаг 4: Проверка автоматической простановки user_id ---')
        session.expire_all()

        db_tasks = session.query(Task).all()
        for task in db_tasks:
            print(
                f'Задача: "{task}" успешно связан!'
                f'Ей автоматически присвоен user_id = {task.user_id}'
            )
        
    except Exception as e:
        session.rollback()
        print(f'Произошла ошибка, транзакция откачена: {e}')
        raise e

    finally:
        session.close()
        print('\nСессия закрыта. База данных в оперативной памяти уничтожена.')

if __name__ == '__main__':
    main()