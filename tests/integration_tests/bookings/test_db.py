from datetime import date
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
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

    new_booking = await db.bookings.add(booking_data)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    await db.bookings.edit(booking_edit_data, id=new_booking.id)
    updated_bookings = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_bookings
    assert updated_bookings.id == new_booking.id
    assert updated_bookings.price != 100

    await db.bookings.delete(id=new_booking.id)
    delete_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not delete_booking
