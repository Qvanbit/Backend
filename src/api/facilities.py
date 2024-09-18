from fastapi import APIRouter, Body

from api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("/facilities")
async def create_facility(
    db: DBDep,
    facility_data: FacilitiesAdd = Body(),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "Success", "data": facility}
