from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    film_id = Column(
        Integer,
        ForeignKey("films.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    film = relationship("Film", back_populates="analysis", uselist=False)

    battery = Column(Float, nullable=True)
    screen = Column(Float, nullable=True)
    memory = Column(Float, nullable=True)
    ram_memory = Column(Float, nullable=True)
    camera = Column(Float, nullable=True)
    performance = Column(Float, nullable=True)
    design = Column(Float, nullable=True)
    quick_charge = Column(Float, nullable=True)
    audio = Column(Float, nullable=True)
    price = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Analysis(id={self.id}, film_id={self.film_id})>"
