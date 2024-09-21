from datetime import date
from fastapi import APIRouter, Body, Query

from api.dependencies import DBDep
from schemas.facilities import RoomFacilityAdd
from schemas.room import RoomAdd, RoomAddRequest, RoomPatch, RoomPathRequest


router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-10-15"),
    date_to: date = Query(example="2024-10-10"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/room/{hotel_id}/{room_id}")
async def get_room_by_id(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(
        hotel_id=hotel_id,
        id=room_id,
    )


@router.post("/add_room")
async def add_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {
        "status": "Success",
        "data": room,
    }


@router.patch("/{hotel_id}/{room_id}")
async def edit_room_part(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPathRequest = Body(),
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status": "Success"}


@router.delete("delete/room/{hotel_id}/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "Success"}


@router.put("/{hotel_id}/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "Success"}
