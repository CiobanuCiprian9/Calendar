from sqlalchemy import or_

import models

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from repositories.database import get_db

router = APIRouter()


@router.get("/all_events")
def list_all_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()

    result = []
    for event in events:
        start_str = event.start_time.isoformat() + "[Europe/Bucharest]"
        end_str = event.end_time.isoformat() + "[Europe/Bucharest]"

        participants_json = [
            {"user_id": p.user_id, "status": p.status}
            for p in event.participants
        ]
        result.append({
            "id": event.id,
            "owner_id": event.owner_id,
            "title": event.title,
            "description": event.description,
            "start_time": start_str,
            "end_time": end_str,
            "location": event.location,
            "participants": participants_json,
        })

    return result


@router.get("/my_events")
def list_events_by_id(db: Session = Depends(get_db), user_id: int | None = Query(None), ):
    event_query = db.query(models.Event)

    if user_id is not None:
        event_query = (
            event_query.outerjoin(models.EventParticipant)
            .filter(
                or_(models.Event.owner_id == user_id,
                    models.EventParticipant.user_id == user_id,
                    )
            )
            .distinct()
        )

    my_events = event_query.all()

    result = []
    for event in my_events:
        start_str = event.start_time.isoformat() + "[Europe/Bucharest]"
        end_str = event.end_time.isoformat() + "[Europe/Bucharest]"

        participants_json = [
            {"user_id": participant.user_id, "status": participant.status}
            for participant in event.participants
        ]

        result.append(
            {
                "id": event.id,
                "owner_id":event.owner_id,
                "title": event.title,
                "description":event.description,
                "start_time":start_str,
                "end_time":end_str,
                "location":event.location,
                "participants":participants_json,
            }
        )

    return result