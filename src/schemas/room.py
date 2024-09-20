from pydantic import BaseModel, ConfigDict, Field


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities_ids: list[int] | None = Field(None)

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    
class Room(RoomAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class RoomPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)