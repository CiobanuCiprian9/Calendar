from datetime import datetime, timezone, date
from typing import Optional, List
from sqlalchemy.orm import Session

import models


class Events:
    def __init__(self,db: Session):
        self.db=db

    def _make_datetime_from_time_str(self, t_str: str, d: Optional[date] = None) -> datetime:
        if d is None:
            d = date.today()

        hour, minute = map(int, t_str.split(":"))

        dt = datetime(d.year, d.month, d.day, hour, minute)

        dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def create_event(self,
                     *,
                     owner_id: int,
                     title: str,
                     start_time: str,
                     end_time: str,
                     description: Optional[str]= None,
                     location: Optional[str]= None,
                     participant_ids: Optional[List[int]]= None) -> models.Event:

        start_dt = self._make_datetime_from_time_str(start_time)
        end_dt = self._make_datetime_from_time_str(end_time)

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

        event.participants=participants

        return event

    def get_event(self):
        pass

    def delete_event(self):
        pass