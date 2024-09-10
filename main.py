from fastapi import FastAPI
import uvicorn

from gyms import router as router_gym

app = FastAPI()

app.include_router(router_gym)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
