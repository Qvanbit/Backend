from fastapi import Body, HTTPException, Query, APIRouter

from schemas.hotels import Gym, GymPatch

router = APIRouter(prefix="/hotels", tags=["Спортзалы"])


gyms = [
    {"id": 1, "title": "Spirit", "city": "Москва"},
    {"id": 2, "title": "Геракл", "city": "Сызрань"},
    {"id": 3, "title": "Xfit", "city": "Казань"},
    {"id": 4, "title": "Dorn", "city": "Москва"},
    {"id": 5, "title": "Volley", "city": "Краснодар"},
    {"id": 6, "title": "Novell", "city": "Сочи"},
    {"id": 7, "title": "Fitnessplan", "city": "Новосибирск"}
]


@router.get("/")
def get_gyms(
    id: int | None = Query(default=None, description="Id Спортазала"),
    title: str | None = Query(default=None, description="Название спортазала"),
    page: int | None = Query(default=1, description="Страницы"),
    per_page: int | None = Query(default=2, description="Количество запросов"),
):
    filtered_gyms = [gym for gym in gyms if (title is None or gym["title"] == title) and (id is None or gym["id"] == id)]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_gyms = filtered_gyms[start:end]
    
    if len(paginated_gyms) == 0 and page > 1:
        raise HTTPException(status_code=404, detail="Page not found")

    return {
        "page": page,
        "per_page": per_page,
        "total": len(filtered_gyms),
        "gyms": paginated_gyms,
    }


@router.put("/{gym_id}")
def update_gym(
    gym_id: int,
    gym_data: Gym,
):
    global gyms
    gym = [gym for gym in gyms if gym["id"] == gym_id][0]
    if gym:
        gym["title"] = gym_data.title
        gym["city"] = gym_data.city
        return {"status": "Success"}
    else:
        return {"status": "Gym not found"}


@router.patch(
    "/{gym_id}",
    summary="Частичное обновление данных о спортзале",
    description="Тут можно частично обновить данных о спортзале",
)
def update_gym_partial(gym_id: int, gym_data: GymPatch):
    global gyms
    gym = [gym for gym in gyms if gym["id"] == gym_id][0]
    if gym:
        if gym_data.title:
            gym["title"] = gym_data.title
        if gym_data.city:
            gym["city"] = gym_data.city
        return {"status": "Success"}
    else:
        return {"status": "Gym not found"}


@router.post("/")
def create_gym(
    gym_data: Gym = Body(
        openapi_examples={
            "1": {
                "summary": "Спортзал",
                "value": {
                    "title": "Odek",
                    "city": "Kazan",
                },
            },
            "2": {
                "summary": "Спортзал2",
                "value": {
                    "title": "Miro",
                    "city": "Sochi",
                },
            }
        }
    ),
):
    global gyms
    gyms.append(
        {
            "id": gyms[-1]["id"] + 1,
            "title": gym_data.title,
            "city": gym_data.city,
        }
    )
    return {"status": "Success"}


@router.delete("/{gym_id}")
def delete_gym(gym_id: int):
    global gyms
    gyms = [gym for gym in gyms if gym["id"] != gym_id]
    return {"status": "Success"}
