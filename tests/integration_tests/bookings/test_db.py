from datetime import date
from src.schemas.bookings import BookingAdd


async def test_add_bookings(db):
    user_id = (await db.users.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=1,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    
    booking_edit_data = BookingAdd(
        user_id=user_id,
        room_id=2,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=30),
        price=1000,
    )

    await db.bookings.add(booking_data)
    await db.bookings.get_all()
    await db.bookings.edit(booking_edit_data)
    await db.bookings.delete()
    
    await db.commit()