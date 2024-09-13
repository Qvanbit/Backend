from sqlalchemy import func, select

from schemas.hotels import Hotel
from src.models.hotels import HotelsORM
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(self, location, title, limit, offset) -> list[Hotel]:
        query = select(HotelsORM)
        if title:
            query = query.filter(
                func.lower(HotelsORM.title).contains(title.strip().lower())
            )
        if location:
            query = query.filter(
                func.lower(HotelsORM.location).contains(location.strip().lower())
            )
        query = query.limit(limit=limit).offset(offset=offset)
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]