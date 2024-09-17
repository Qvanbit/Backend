from fastapi import APIRouter, Body, Query

from api.dependencies import DBDep
from schemas.room import RoomAdd, RoomPatch


router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/rooms/{hotel_id}")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    title: str | None = Query(default=None, description="Название команты"),
):
    return await db.rooms.get_all(
        hotel_id=hotel_id,
        title=title,
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
    return {"status": "Success"}


@router.delete("delete/room/{hotel_id}/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    return {"status": "Success"}


@router.put("/{hotel_id}/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAdd = Body(),
):
    await db.rooms.edit(room_data, hotel_id=hotel_id, id=room_id)
    return {"status": "Success"}
