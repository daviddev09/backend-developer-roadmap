from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
# ===========================
#       Create Schemas
# ===========================
class UserCreate(BaseModel):
    username: str
    email: EmailStr


class PostCreate(BaseModel):
    text: str


class TagCreate(BaseModel):
    tag_name: str

# ===========================
#       Read Schemas
# ===========================


class UserRead(BaseModel):
    id: int
    username:str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class PostRead(BaseModel):
    id: int
    text: str
    created_at: datetime
    likes: int
    
    model_config = ConfigDict(from_attributes=True)


class TagRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserLiteRead(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class TagLiteRead(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserPostRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: list[PostRead]
    model_config = ConfigDict(from_attributes=True)


class PostUserTagRead(BaseModel):
    text:str
    created_at: datetime
    likes:int

    user: UserLiteRead
    tags: list[TagLiteRead]

