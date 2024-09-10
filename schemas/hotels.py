from pydantic import BaseModel, Field


class Gym(BaseModel):
    title: str
    city: str
    
class GymPatch(BaseModel):
    title: str | None =  Field(None)
    city: str | None = Field(None)