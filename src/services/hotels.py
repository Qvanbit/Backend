from datetime import date
from src.schemas.hotels import HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            offset=per_page * (pagination.page - 1),
            limit=per_page,
        )

    async def get_one_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data=data)
        await self.db.commit()
        return hotel
    
    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        
    async def edit_hotel(self, hotel_id: int, data: HotelAdd):
        await self.db.hotels.edit(data=data, id=hotel_id)
        await self.db.commit()
        
    async def edit_hotel_partial(self, hotel_id: int, data: HotelPatch, exclude_unset: bool = False):
        await self.db.hotels.edit(data=data, id=hotel_id, exclude_unset=exclude_unset)
        await self.db.commit()
