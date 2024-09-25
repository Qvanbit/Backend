from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from tests.conftest import async_session_maker


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Sochi")
    await db.hotels.add(hotel_data)
    await db.commit()