from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.hotels import router as router_gym
from api.auth import router as router_auth
from api.rooms import router as router_rooms
from api.bookings import router as router_bookings
from api.facilities import router as router_facilities
app = FastAPI()


app.include_router(router_auth)
app.include_router(router_gym)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
