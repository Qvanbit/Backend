from datetime import date
from services.base import BaseService


class RoomService(BaseService):
    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_room_by_id(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_or_none_with_rels(
            hotel_id=hotel_id,
            room_id=room_id,
        )
