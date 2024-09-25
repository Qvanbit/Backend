import pytest
from dotenv import load_dotenv
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings
from src.database import Base, engine_new_pool
from src.models import *

URL = "postgresql+asyncpg://postgres:password@localhost:5432/gg"

engine_new_pool = create_async_engine(
        url=URL, poolclass=NullPool
    )
async_session_maker = async_sessionmaker(bind=engine_new_pool, expire_on_commit=False)

@pytest.fixture(scope="session", autouse=True)
async def async_main():
    
    async with engine_new_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)