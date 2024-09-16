from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.hotels import router as router_gym
from api.auth import router as router_auth
from api.rooms import router as router_rooms
app = FastAPI()


app.include_router(router_auth)
app.include_router(router_gym)
app.include_router(router_rooms)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
