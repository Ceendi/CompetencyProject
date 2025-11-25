import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String(200), index=True, nullable=False)

    status = Column(String(50), nullable=False, default='pending', index=True)

    error_message = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    film_id = Column(Integer, ForeignKey("films.id"), nullable=True, unique=False)

    film = relationship("Film")

    def __repr__(self):
        return f"<Job(id={self.id}, status='{self.status}', url='{self.url[:30]}...')>"
