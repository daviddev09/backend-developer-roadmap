from models.user import User
from schemas.user import UserRead


def serialize_the_model(user: User) -> str:
    return UserRead.model_validate(user).model_dump_json(indent=2)
    

user = User(id=1, email='daviddev09@example.com', password_hash='d2009a2009v20009i2009d')

print(serialize_the_model(user))
print(type(serialize_the_model(user)))