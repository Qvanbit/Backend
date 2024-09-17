from datetime import date

from repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.schemas.room import Room
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_bi_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))