from src.models.facilities import FacilitiesORM, RoomFacilitiesORM
from src.schemas.facilities import Facilities, RoomFacility
from src.repositories.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facilities
    
class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesORM
    schema = RoomFacility