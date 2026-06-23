from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
# ===========================
#       Create Schemas
# ===========================


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        description="Уникальный логин пользователя в системе", 
        examples=["daviddev"]
    )
    email: EmailStr = Field(
        ..., 
        description="Рабочий адрес электронной почты", 
        examples=["david@example.com"]
    )

    model_config =ConfigDict(json_schema_extra = {"example": {"username": "daviddev",
                "email": "david@example.com"}})


class PostCreate(BaseModel):
    text: str = Field(..., description='Текст вашего поста', examples=['Я учусь в день по 8-10 часов'])
    model_config = ConfigDict(json_schema_extra={'example':{'text': 'Я учусь в день по 8-10 часов'}})


# ===========================
#       Read Schemas
# ===========================

class UserLiteRead(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class TagLiteRead(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class PostLiteRead(BaseModel):
    id: int
    text: str
    created_at: datetime
    likes: int
    
    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    id: int
    username:str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserPostRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: list[PostLiteRead]
    model_config = ConfigDict(from_attributes=True)


class PostUserTagRead(BaseModel):
    id: int
    text: str
    created_at: datetime
    likes: int

    user: UserLiteRead
    tags: list[TagLiteRead]

    model_config = ConfigDict(from_attributes=True)


# ===========================
#       Update Schema
# ===========================


class PostUpdate(BaseModel):
    new_text: str|None = Field(default=None, description='Новый текст')
    new_tags: str|None = Field(default=None, description='Новые теги')