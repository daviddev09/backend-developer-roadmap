from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Task

DATABASE_URL = 'sqlite:///app.db'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def main():
    print('----- Создание таблиц -----')

    session = SessionLocal()

    try:
        print('\n--- Шаг 1: Создание пользователя ---')
        user = User(name='David')

        print('\n--- Шаг 2: Создание задач ---')
        task1 = Task(title='Изучить SQL')
        task2 = Task(title='Изучить SQLAlchemy ORM')
        task3 = Task(title='Оптимизировать БД')

        print('\n--- Шаг 3: Добавление задач пользователю ---')
        user.tasks.append(task1)
        user.tasks.append(task2)
        user.tasks.append(task3)

        session.add(user)

        print('\n--- Шаг 4: Сохранение данных ---')
        session.commit()
        print('Данные успешно сохранены')

        print('\n--- Шаг 5: Извлечение пользователя из БД ---')
        db_user = (
            session.query(User)
            .filter_by(id=user.id)
            .one()
        )

        print(f'Пользователь: {db_user}')
        print('Его задачи:')

        for task in db_user.tasks:
            print(task)

        print('\n--- Шаг 6: Удаление одной задачи ---')

        task_for_delete = db_user.tasks[1]

        print(f'Удаляем: {task_for_delete}')

        db_user.tasks.remove(task_for_delete)

        print('\n--- Шаг 7: Сохранение изменений ---')
        session.commit()
        print('Изменения сохранены')

        print('\n--- Шаг 8: Проверка оставшихся задач ---')

        db_tasks = session.query(Task).all()

        for task in db_tasks:
            print(
                f'Задача: "{task}" '
                f'имеет user_id = {task.user_id}'
            )

    except Exception as e:
        session.rollback()
        print(f'Произошла ошибка: {e}')
        raise

    finally:
        session.close()
        print('\nСессия закрыта')


if __name__ == '__main__':
    main()