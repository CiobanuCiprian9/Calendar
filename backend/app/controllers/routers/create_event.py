from datetime import date

from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session

from controllers.helpers.event_mapper import event_to_response
from repositories.database import get_db
from services.event_service import Events

router=APIRouter()

@router.post("/create_event")
async def create_event(
        request: Request,
        db: Session= Depends(get_db),
        user_id: int | None = Query(None),
    ):
    body = await request.json()

    title = body.get("title")
    event_date_str = body.get("event_date")
    start_time_str = body.get("start_time")
    end_time_str = body.get("end_time")
    description = body.get("description")
    location = body.get("location")
    participant_ids = body.get("participant_ids") or []

    year, month, day = map(int, event_date_str.split("-"))
    event_date = date(year, month, day)

    service = Events(db)

    event = service.create_event(
        owner_id=user_id,
        title=title,
        event_date=event_date,
        start_time=start_time_str,
        end_time=end_time_str,
        description=description,
        location=location,
        participant_ids=participant_ids,
    )

    return event_to_response(event)