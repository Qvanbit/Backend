from datetime import date
from fastapi import APIRouter, Body, Query

from api.dependencies import DBDep
from schemas.room import RoomAdd, RoomPatch


router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-10-15"),
    date_to: date = Query(example="2024-10-10"),
):
    return await db.rooms.get_filtered_bi_time(
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
    db: DBDep,
    room_data: RoomAdd = Body(),
):
    room = await db.rooms.add(room_data)
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
    room_data: RoomPatch = Body(),
):
    await db.rooms.edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
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
    room_data: RoomAdd = Body(),
):
    await db.rooms.edit(room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "Success"}
