from typing import Annotated
from fastapi import Body, HTTPException, Query, APIRouter

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Спортзалы"])


hotels = [
    {"id": 1, "title": "Spirit", "city": "Москва"},
    {"id": 2, "title": "Геракл", "city": "Сызрань"},
    {"id": 3, "title": "Xfit", "city": "Казань"},
    {"id": 4, "title": "Dorn", "city": "Москва"},
    {"id": 5, "title": "Volley", "city": "Краснодар"},
    {"id": 6, "title": "Novell", "city": "Сочи"},
    {"id": 7, "title": "Fitnessplan", "city": "Новосибирск"}
]


@router.get("/")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, description="Id Отеля"),
    title: str | None = Query(default=None, description="Название Отеля"),
):
    filtered_hotel = [hotel for hotel in hotels if (title is None or hotel["title"] == title) and (id is None or hotel["id"] == id)]

    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    paginated_hotel = filtered_hotel[start:end]
    
    if len(paginated_hotel) == 0 and pagination.page > 1:
        raise HTTPException(status_code=404, detail="Page not found")

    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": len(filtered_hotel),
        "hotels": paginated_hotel,
    }


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
def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Отель1",
                "value": {
                    "title": "Odek",
                    "city": "Kazan",
                },
            },
            "2": {
                "summary": "Отель2",
                "value": {
                    "title": "Miro",
                    "city": "Sochi",
                },
            }
        }
    ),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "city": hotel_data.city,
        }
    )
    return {"status": "Success"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Success"}
