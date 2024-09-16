from fastapi import APIRouter, Body, Query

from api.open_api_examples import rooms_example
from repositories.rooms import RoomsRepository
from schemas.room import RoomAdd, RoomPatch
from src.database import async_session_maker


router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/rooms/{hotel_id}")
async def get_rooms(
    hotel_id: int,
    title: str | None = Query(default=None, description="Название команты"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session=session).get_all(
            hotel_id=hotel_id,
            title=title,
        )


@router.get("/room/{hotel_id}/{room_id}")
async def get_room_by_id(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session=session).get_one_or_none(
            hotel_id=hotel_id,
            id=room_id,
        )


@router.post("/add_room")
async def add_room(
    room_data: RoomAdd = Body(),
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session=session).add(room_data)
        await session.commit()
        return {
            "status": "Success",
            "data": room,
        }

@router.patch('/{hotel_id}/{room_id}')
async def edit_room_part(
    hotel_id: int,
    room_id: int, 
    room_data: RoomPatch = Body(),
):
    async with async_session_maker()  as session:
        await RoomsRepository(session=session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "Success"}
    
    
@router.delete('delete/room/{hotel_id}/{room_id}')
async def delete_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session=session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "Success"}
    
@router.put('/{hotel_id}/{room_id}')
async def edit_room(
    hotel_id: int,
    room_id: int, 
    room_data: RoomAdd = Body(),
):
    async with async_session_maker() as session:
        await RoomsRepository(session=session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "Success"}