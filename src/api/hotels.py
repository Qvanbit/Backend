from fastapi import Body, Query, APIRouter

from api.open_api_examples import hotel_example
from src.repositories.hotels import HotelsRepository

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(default=None, description="Локация отеля"),
    title: str | None = Query(default=None, description="Название Отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session=session).get_all(
            location=location,
            title=title,
            offset=per_page * (pagination.page - 1),
            limit=per_page,
    )
        
        
@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session=session).get_one_or_none(id=hotel_id)

@router.put("/{gym_id}")
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
):
    async with async_session_maker() as session:
        await HotelsRepository(session=session).edit(data=hotel_data, id=hotel_id)
        await session.commit()
        return {"status": "Success"}     


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут можно частично обновить данных об отеле",
)
async def update_hotel_partial(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session=session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
        return {"status": "Success"}


@router.post("/")
async def create_hotel(
    hotel_data: HotelAdd = Body(),
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session=session).add(hotel_data)
        await session.commit()
        return {"status": "Success",
                "data": hotel,
                }


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session=session).delete(id=hotel_id)
        await session.commit()
        return {"status": "Success"}

