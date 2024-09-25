from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class RoomsORM(Base):
    __tablename__ = "rooms"
    
    id: Mapped[int]  = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    
    facilities: Mapped[list["FacilitiesORM"]] = relationship( # type: ignore
        back_populates="rooms",
        secondary="room_facilities",
    )