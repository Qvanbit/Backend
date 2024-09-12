from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    city: str
    
class HotelPatch(BaseModel):
    title: str | None =  Field(None)
    city: str | None = Field(None)