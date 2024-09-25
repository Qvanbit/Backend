from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class HotelsORM(Base):
    __tablename__ = "hotels"
    
    id: Mapped[int]  = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100), nullable=False)
    location: Mapped[str]