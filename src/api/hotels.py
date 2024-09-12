from fastapi import Body, Query, APIRouter

from sqlalchemy import insert, select

from src.models.hotels import HotelsORM
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Спортзалы"])


@router.get("/")
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(default=None, description="Локация отеля"),
    title: str | None = Query(default=None, description="Название Отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.filter_by(title=title)
        if location:
            query = query.filter(HotelsORM.location.like(f"%Сочи%")) # type: ignore
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

@router.put("/{gym_id}")
def update_hotel(
    hotel_id: int,
    hotel_data: Hotel,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel:
        hotel["title"] = hotel_data.title
        hotel["city"] = hotel_data.city
        return {"status": "Success"}
    else:
        return {"status": "Hotel not found"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут можно частично обновить данных об отеле",
)
def update_hotel_partial(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel:
        if hotel_data.title:
            hotel["title"] = hotel_data.title
        if hotel_data.city:
            hotel["city"] = hotel_data.city
        return {"status": "Success"}
    else:
        return {"status": "Hotel not found"}


@router.post("/")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Отель1",
                "value": {
                    "title": "Odek",
                    "location": "Kazan",
                },
            },
            "2": {
                "summary": "Отель2",
                "value": {
                    "title": "Miro",
                    "location": "Sochi",
                },
            },
        }
    ),
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()
        return {"status": "Success"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Success"}
