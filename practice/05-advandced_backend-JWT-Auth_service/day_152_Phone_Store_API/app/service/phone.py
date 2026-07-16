from app.core.uow import UnitOfWork
from app.schemes.phone import PhoneCreate, PhoneUpdate
from app.exceptions.exception import EntityNotFound, UniqueError

class PhoneService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_phone(self, data: PhoneCreate):
        async with self.uow:
            phones = await self.uow.phones.get_phones_by_name(data.name)
            for phone in phones:
                if phone.name and data.name and phone.storage == data.storage:
                    raise UniqueError(
                        detail="Такой телефон уже существует в БД."
                        " Если хотите изменить количество, воспользуйтесь эндпоинтом: Change phone data"
                    )
            phone = await self.uow.phones.add_phone(data=PhoneCreate.model_dump(data))
            await self.uow.commit()
            return phone
        

    async def get_phone_by_id(self, phone_id: int):
        async with self.uow:
            phone = await self.uow.phones.get_phone_by_id(phone_id)
            if phone:
                return phone
            raise EntityNotFound(detail='Телефон с таким ID не найден')
        
    async def get_phones(self, last_phone_id: int):
        async with self.uow:
            return await self.uow.phones.get_paginated_phones(last_phone_id, limit=20)
        
    async def search_phones(self, phone_name: str):
        async with self.uow:
            phones = await self.uow.phones.get_phones_by_name(phone_name)
            if phones:
                return phones
            raise EntityNotFound(detail=f'По запросу: {phone_name} ничего не найдено')
        
        
    async def update_phone(self, phone_id: int, phone_update: PhoneUpdate):
        async with self.uow:
            if not await self.uow.phones.check_phone_exists(phone_id):
                raise EntityNotFound(detail='Phone not found')
            
            phone = await self.uow.phones.change_phone_data(phone_id, PhoneUpdate.model_dump(phone_update))
            await self.uow.commit()
            return phone
        
    async def delete_phone(self, phone_id: int):
        async with self.uow:
            if not await self.uow.phones.check_phone_exists(phone_id):
                raise EntityNotFound(detail='Phone not found')
            await self.uow.phones.delete_phone(phone_id)
            await self.uow.commit()
            return
