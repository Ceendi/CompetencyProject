from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String(200), unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    transcribed_text = Column(String, nullable=True)

    analysis = relationship(
        "Analysis",
        back_populates="film",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Film(id={self.id}, url='{self.url[:30]}...')>"
