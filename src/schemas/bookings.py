from datetime import date

from pydantic import BaseModel, Field


class BookingsAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date

class Bookings(BookingsAdd):
    id: int
    
    
class BokingsPatch(BaseModel):
    ...