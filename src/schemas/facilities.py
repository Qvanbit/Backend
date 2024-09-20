from pydantic import BaseModel, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str
    
class Facilities(FacilitiesAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
    
class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int
    
class RoomFacility(RoomFacilityAdd):
    id: int