import pytest
from typing import TypedDict


class UserType(TypedDict):
   name: str
   graduation: str
   target: str
   is_active: bool


class DbType(TypedDict):
   db_status: str
   db_data: list[UserType]


@pytest.fixture
def create_test_user() -> UserType:
    return {
        'name': 'daviddev',
        'graduation': 'school_pupil',
        'target': 'backend_junior',
        'is_active': True
    }

@pytest.fixture
def get_db(create_test_user: UserType):
    user = create_test_user
    db: DbType = {
        'db_status': 'connected',
        'db_data': [user]
    }
    yield db

    db['db_data'].clear()
    db['db_status'] = 'disconnected'

@pytest.fixture(scope='session')
def read_configuration():
    import os
    import dotenv

    dotenv.load_dotenv()
    return os.getenv('PASSWORD', '12345678')