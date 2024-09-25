from datetime import date
from fastapi import Body, Query, APIRouter

from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(default=None, description="Локация отеля"),
    title: str | None = Query(default=None, description="Название Отеля"),
    date_from: date = Query(example="2024-10-01"),
    date_to: date = Query(example="2024-10-31"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        offset=per_page * (pagination.page - 1),
        limit=per_page,
    )

@router.get("/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int,
    db: DBDep,
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd,
):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "Success"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут можно частично обновить данных об отеле",
)
async def update_hotel_partial(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "Success"}


@router.post("/")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {
        "status": "Success",
        "data": hotel,
    }


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "Success"}


