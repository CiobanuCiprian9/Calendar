from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class EventParticipant(Base):
    __tablename__="Event_Participants"

    id=Column(Integer,primary_key=True)

    event_id=Column(Integer,ForeignKey("Events.id"),nullable=False)
    user_id=Column(Integer,ForeignKey("Users.id"),nullable=False)

    event=relationship("Event",back_populates="participants")
    user=relationship("User",back_populates="events_participating")