from app.models.phone import Phone

from typing import Any

from sqlalchemy import select, exists, delete
from sqlalchemy.ext.asyncio import AsyncSession


class PhoneRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_phone(self, data: dict[str, Any]):
        phone = Phone(**data)
        
        self.session.add(phone)
        await self.session.flush()
        return phone


    async def check_phone_exists(self, phone_id: int):
        result = await self.session.execute(select(exists(Phone).where(Phone.id == phone_id)))
        return result.scalar()

    async def get_phones_by_name(self, name: str):
        phone = await self.session.scalars(select(Phone).where(Phone.name.ilike(f'%{name}%')))
        
        return phone.all()
    
    async def get_phone_by_id(self, phone_id: int):
        result = await self.session.execute(select(Phone).where(Phone.id == phone_id))
        phone = result.scalar_one_or_none()
        if not phone:
            return None
        return phone
        
    
    async def get_paginated_phones(self,last_phone_id: int, limit: int):
        stmt = select(Phone)

        if last_phone_id > 0:
            stmt = stmt.where(Phone.id > last_phone_id)
        
        stmt = stmt.order_by(Phone.id.asc()).limit(limit)
        result = await self.session.scalars(stmt)
        return result.all()
    
    async def change_phone_data(self, phone_id:int, new_data: dict[str, Any]):
        phone = await self.get_phone_by_id(phone_id)
        for key, value in new_data.items():
            if hasattr(phone, key):
                setattr(phone, key, value)
        await self.session.flush()
        return phone
        
    async def delete_phone(self, phone_id: int):
        await self.session.execute(delete(Phone).where(Phone.id == phone_id))
        return