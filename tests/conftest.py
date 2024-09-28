import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient
import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.api.dependencies import get_db
from src.main import app
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService
from src.schemas.room import RoomAdd
from src.schemas.hotels import HotelAdd
from src.database import Base, engine_new_pool
from src.models import *
from src.utils.db_manager import DBManager
from src.database import async_session_maker_new_pool

URL = "postgresql+asyncpg://postgres:password@localhost:5432/gg"

engine_new_pool = create_async_engine(url=URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(bind=engine_new_pool, expire_on_commit=False)


@pytest.fixture()
async def db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db
        
async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_new_pool) as db:
        yield db

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine_new_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
        
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)
    
    with open("tests/mock_users.json", encoding="utf-8") as file_users:
        users = json.load(file_users)
        
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]
    users = [UserRequestAdd.model_validate(user) for user in users]
    for user in users:
        hashed_password = AuthService().hash_password(user.password)
        new_user_data = UserAdd(email=user.email, hashed_password=hashed_password)
        async with DBManager(session_factory=async_session_maker) as db_:
            await db_.users.add(new_user_data)  
            await db_.commit()
    
    async with DBManager(session_factory=async_session_maker) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()
        
        
@pytest.fixture(scope="session")
async def ac() -> AsyncClient: # type: ignore
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        yield ac
        
app.dependency_overrides[get_db] = get_db_null_pool
        
@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "alexander@gmail.com",
            "password": "1234",
        },
    )
    assert ac.cookies["access_token"]
    yield ac