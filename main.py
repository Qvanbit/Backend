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
