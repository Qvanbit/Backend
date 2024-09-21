from models.bookings import BookingsORM
from src.schemas.facilities import Facilities
from src.models.facilities import FacilitiesORM
from src.models.users import UserORM
from src.schemas.bookings import Booking
from src.schemas.users import User
from src.schemas.room import Room, RoomWithRels
from src.models.rooms import RoomsORM
from src.models.hotels import HotelsORM
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel
    
class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room
    
class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels
    
class UserDataMapper(DataMapper):
    db_model = UserORM
    schema = User
    
class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking
    
class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facilities