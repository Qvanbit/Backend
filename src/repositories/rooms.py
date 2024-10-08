from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.mappers.base import DataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsORM
    smapper: DataMapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]

    async def get_one_or_none_with_rels(self, hotel_id: int, room_id: int):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(hotel_id=hotel_id, id=room_id)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
