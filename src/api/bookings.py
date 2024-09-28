from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from src.exceptions import ObjectNotFoundException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/")
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/bookings/me")
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_all(
        user_id=user_id,
    )


@router.post("/")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
