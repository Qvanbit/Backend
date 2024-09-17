from models.bookings import BookingsORM
from schemas.bookings import Booking
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking
