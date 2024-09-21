from datetime import date

from sqlalchemy import func, select

from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.mappers.base import DataMapper
from src.models.rooms import RoomsORM
from src.repositories.utils import rooms_ids_for_booking
from schemas.hotels import Hotel
from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper: DataMapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsORM).filter(HotelsORM.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(
                func.lower(HotelsORM.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsORM.title).contains(title.strip().lower())
            )
        query = query.limit(limit=limit).offset(offset=offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars()]
