from sqlalchemy import func, select
from models.rooms import RoomsORM
from schemas.room import Room
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_all(self, title, hotel_id) -> list[Room]:
        query = select(RoomsORM).where(RoomsORM.hotel_id == hotel_id)
        if title:
            query = query.filter(
                func.lower(RoomsORM.title).contains(title.strip().lower())
            )
        result = await self.session.execute(query)
        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]
