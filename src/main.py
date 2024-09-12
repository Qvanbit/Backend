from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from api.hotels import router as router_gym
from src.config import settings

app = FastAPI()



app.include_router(router_gym)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
