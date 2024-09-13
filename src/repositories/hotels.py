from sqlalchemy import func, select

from src.models.hotels import HotelsORM
from src.repositories.base import BasePepository


class HotelsRepository(BasePepository):
    model = HotelsORM

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsORM)
        if title:
            query = query.filter(
                func.lower(HotelsORM.title).contains(title.strip().lower())
            )
        if location:
            query = query.filter(
                func.lower(HotelsORM.location).contains(location.strip().lower())
            )
        query = query.limit(limit=limit).offset(offset=offset)
        result = await self.session.execute(query)
        return result.scalars().all()