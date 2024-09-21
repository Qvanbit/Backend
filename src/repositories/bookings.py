from sqlalchemy import func, select
from models.bookings import BookingsORM
from src.repositories.mappers.mappers import BookingDataMapper
from schemas.bookings import Booking
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper