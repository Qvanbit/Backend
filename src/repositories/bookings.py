from pydantic import BaseModel
from sqlalchemy import insert

from models.bookings import BookingsORM
from schemas.bookings import Bookings
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = BookingsORM
    schema = Bookings

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)
    
