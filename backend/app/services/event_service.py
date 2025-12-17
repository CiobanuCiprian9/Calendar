from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

import models
from domain.event_bus import event_bus

class Events:
    def __init__(self,db: Session):
        self.db=db

    def _make_datetime_from_time_str(self, t_str: str, d: date) -> datetime:
        hour, minute = map(int, t_str.split(":"))

        return datetime(d.year, d.month, d.day, hour, minute,tzinfo=timezone.utc)

    def create_event(self,
                     *,
                     owner_id: int,
                     title: str,
                     event_date:date,
                     start_time: str,
                     end_time: str,
                     description: Optional[str]= None,
                     location: Optional[str]= None,
                     participant_ids: Optional[List[int]]= None) -> models.Event:

        start_dt = self._make_datetime_from_time_str(start_time,event_date)
        end_dt = self._make_datetime_from_time_str(end_time,event_date)

        if end_dt <= start_dt:
            raise ValueError("end_time must be after start_time")

        event=models.Event(
            owner_id=owner_id,
            title=title.strip(),
            description=description,
            start_time=start_dt,
            end_time=end_dt,
            location=location,
        )
        self.db.add(event)
        self.db.flush()

        participants=[]
        for uid in participant_ids:
            participant=models.EventParticipant(
                event_id=event.id,
                user_id=uid,
            )
            self.db.add(participant)
            participants.append(participant)

        self.db.commit()
        self.db.refresh(event)

        event = (
            self.db.query(models.Event)
            .options(
                joinedload(models.Event.participants).joinedload(models.EventParticipant.user)
            )
            .filter(models.Event.id == event.id)
            .first()
        )

        event.participants=participants
        event_bus.publish("event_created", {"event": event})

        return event

    def get_all_events(self):
        return (
            self.db.query(models.Event)
            .options(
                joinedload(models.Event.participants).joinedload(models.EventParticipant.user)
            )
            .all()
        )

    def get_events_for_user(self, user_id: Optional[int]):
        query = (
            self.db.query(models.Event)
            .options(
                joinedload(models.Event.participants).joinedload(models.EventParticipant.user)
            )
        )

        if user_id is not None:
            from sqlalchemy import or_
            query = (
                query.outerjoin(models.EventParticipant)
                .filter(
                    or_(
                        models.Event.owner_id == user_id,
                        models.EventParticipant.user_id == user_id,
                    )
                )
                .distinct()
            )

        return query.all()

    def delete_event(self):
        pass