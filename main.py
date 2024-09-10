from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

gyms = [
    {"id": 1, "title": "Spirit", "city": "Москва"},
    {"id": 2, "title": "Геракл", "city": "Сызрань"},
]


@app.get("/gyms")
def get_gyms(
    id: int | None = Query(default=None, description="Id Спортазала"),
    title: str | None = Query(default=None, description="Название спортазала"),
):
    return [gym for gym in gyms if gym["title"] == title or gym["id"] == id]

@app.put('/gyms/{gym_id}')
def update_gym(
        gym_id: int,
        title: str = Body(embed=True),
        city: str = Body(embed=True),
):
        global gyms
        gym = next((gym for gym in gyms if gym["id"] == gym_id), None)
        if gym:
            gym["title"] = title
            gym["city"] = city
            return {"status": "Success"}
        else:
            return {"status": "Gym not found"}

@app.patch('/gyms/{gym_id}')
def update_gym_partial(
        gym_id: int,
        title: str | None = Body(embed=True, default=None),
        city: str | None  = Body(embed=True, default=None),
):
        global gyms
        gym = next((gym for gym in gyms if gym["id"] == gym_id), None)
        if gym:
            if title:
                gym["title"] = title
            if city:
                gym["city"] = city
            return {"status": "Success"}
        else:
            return {"status": "Gym not found"}
        

@app.post("/gyms")
def create_gym(
        title: str = Body(embed=True),
):
    global gyms
    gyms.append(
        {
            "id": gyms[-1]["id"] + 1,
            "title": title,
        }
    )
    return {"status": "Success"}


@app.delete("/gym/{gym_id}")
def delete_gym(gym_id: int):
    global gyms
    gyms = [gym for gym in gyms if gym["id"] != gym_id]
    return {"status": "Success"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
