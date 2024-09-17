from datetime import date
from fastapi import APIRouter

from api.dependencies import DBDep
from src.models.bookings import BookingsORM

router = APIRouter(prefix="/booking", tags=["Бронирование"])


@router.post("/")
async def create_booking(db: DBDep, room_id: int, date_from: date, date_to: date):
    return await db.bookings.add(
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=BookingsORM.total_cost,
    )
