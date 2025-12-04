from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)

    first_name=Column(String(100),nullable=False)
    middle_name=Column(String(100),nullable=True)
    last_name=Column(String(100),nullabler=False)

    email=Column(String(100),nullable=False,unique=True)
    password_hash=Column(String(100),nullable=False)

    timezone=Column(String(50),nullable=False)

    events_owned=relationship("Event",back_populates="owner")
    events_participating=relationship("EventParticipant",back_populates="user")
