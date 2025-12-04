from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class Event(Base):
    __tablename__="Events"

    id=Column(Integer,primary_key=True)

    owner_id=Column(Integer,ForeignKey("Users.id"),nullable=False)
    title=Column(String(200),nullable=False)
    description=Column(Text,nullable=True)

    start_time=Column(DateTime(timezone=True),nullable=False)
    end_time=Column(DateTime(timezone=True),nullable=False)

    location=Column(String,nullable=True)

    owner=relationship("User",back_populates="events_owned")
    participants=relationship("EventParticipant",back_populates="event")