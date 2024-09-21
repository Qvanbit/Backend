from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base


class FacilitiesORM(Base):
    __tablename__ = "facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    
    rooms: Mapped[list["RoomsORM"]] = relationship( # type: ignore
        back_populates="facilities",
        secondary="room_facilities",
    )
    
class RoomFacilitiesORM(Base):
    __tablename__ = "room_facilities"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))