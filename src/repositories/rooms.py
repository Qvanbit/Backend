from models.rooms import RoomsORM
from src.repositories.base import BasePepository

class RoomsRepository(BasePepository):
    model = RoomsORM