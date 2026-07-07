from models.base import Base

from typing import Type, TypeVar, Generic, Any

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, data: dict[str, Any]):
        try:
            new_obj = self.model(**data)

            self.session.add(new_obj)
            await self.session.commit()
            await self.session.refresh(new_obj)

            return new_obj
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(f'Произошла ошибка: {e}')
            return None
        
    async def get_by_id(self, obj_id: int):
        try:
            result = await self.session.execute(select(self.model).where(self.model.id == obj_id)) # type: ignore
            return result.scalar_one_or_none()
        
        except SQLAlchemyError as e:
            print(f'Произошла ошибка: {e}')
            return None
        
    async def update(self, obj_id: int, data: dict[str, Any]):
        obj = await self.get_by_id(obj_id = obj_id)

        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            await self.session.commit()
            await self.session.refresh(obj)

            return obj
        
    async def delete(self, obj_id: int):
        await self.session.execute(delete(self.model).where(self.model.id == obj_id)) # type: ignore
        await self.session.commit()
        return