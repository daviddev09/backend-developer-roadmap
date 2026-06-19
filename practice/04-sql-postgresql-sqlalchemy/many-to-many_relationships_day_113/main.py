from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Task, Tag, Base


DATABASE_URL = 'sqlite:///app.db'

engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def main():

    Base.metadata.drop_all(engine)
    
    Base.metadata.create_all(engine)
    
    session = SessionLocal()

    try:
        tag1 = Tag(name='# everyday')
        tag3 = Tag(name='# db language')
        tag5 = Tag(name='# necessary')

        print('\n----- Таблицы и теги в памяти созданы -----')

        print('--- Шаг 1: Создание задачи ---')
        task = Task(title='Learn the SQL')

        print('--- Шаг 2: Добавление тэгов к задаче ---')
        task.tags.append(tag1)
        task.tags.append(tag3)
        task.tags.append(tag5)

        print('--- Шаг 3: Передача объектов в сессию ---')
        session.add(task)
        
        print('--- Шаг 4: Физическое сохранение в БД ---')
        session.commit()
        print('Данные успешно сохранены в app.db!')

        print('\n--- Шаг 5: Извлечение задачи из БД ---')
        db_task = (
            session.query(Task)
            .filter_by(id=task.id)
            .one()
        )
        
        print(f'\nЗадача "{db_task.title}" имеет тэги:')
        for tag in db_task.tags:
            print(f' - {tag.name}')

    except Exception as e:
        session.rollback()
        print(f'\n Произошла ошибка: {e}')
        raise

    finally:
        session.close()
        print('\nСессия закрыта')

if __name__ == '__main__':
    main()