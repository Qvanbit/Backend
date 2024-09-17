from sqlalchemy import func, select
from models.bookings import BookingsORM
from schemas.bookings import Booking
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking

    async def get_all(self, user_id) -> list[Booking]:
        query = select(BookingsORM).where(BookingsORM.user_id == user_id)
        
        result = await self.session.execute(query)
        return [Booking.model_validate(booking, from_attributes=True) for booking in result.scalars().all()]