from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from tests.conftest import async_session_maker


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Sochi")
    async with DBManager(session_factory=async_session_maker) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel_data=}")