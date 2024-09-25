from fastapi import APIRouter, Body

from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd
from src.tasks.tasks import test_task



router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
@cache(expire=10)
async def get_all_facilities(db: DBDep):
    test_task.delay()
    return await db.facilities.get_all()

@router.post("/facilities")
async def create_facility(
    db: DBDep,
    facility_data: FacilitiesAdd = Body(),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    

    return {"status": "Success", "data": facility}
