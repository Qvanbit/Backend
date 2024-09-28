from datetime import date
from fastapi import Body, HTTPException, Query, APIRouter

from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException
from src.services.hotels import HotelsService
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch

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
    return await HotelsService(db).get_filtered_by_time(
        pagination=pagination,
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelsService(db).get_one_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель не найден")


@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd,
):
    await HotelsService(db=db).edit_hotel(data=hotel_data, hotel_id=hotel_id)
    return {"status": "Success"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут можно частично обновить данных об отеле",
)
async def update_hotel_partial(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelsService(db=db).edit_hotel_partial(data=hotel_data, hotel_id=hotel_id, exclude_unset=True)
    return {"status": "Success"}


@router.post("/")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(),
):
    hotel = await HotelsService(db).create_hotel(data=hotel_data)
    return {
        "status": "Success",
        "data": hotel,
    }


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelsService(db=db).delete_hotel(hotel_id=hotel_id)
    return {"status": "Success"}
