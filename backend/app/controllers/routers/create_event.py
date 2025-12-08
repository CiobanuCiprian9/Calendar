from datetime import date

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from repositories.database import get_db
from services.event_service import Events

router=APIRouter()


def get_current_user_id() -> int:
    # TODO: înlocuiești cu logica ta reală de auth
    return 1

@router.post("/")
async def event(
        request: Request,
        db: Session= Depends(get_db),
        current_user_id: int= Depends(get_current_user_id),
):
    body = await request.json()

    title = body.get("title")
    event_date_str = body.get("event_date")
    start_time_str = body.get("start_time")
    end_time_str = body.get("end_time")
    description = body.get("description")
    location = body.get("location")
    participant_ids = body.get("participant_ids") or []

    if event_date_str:
        try:
            year, month, day = map(int, event_date_str.split("-"))
            event_date = date(year, month, day)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid event_date format: {event_date_str} (expected YYYY-MM-DD)",
            )


    service = Events(db)
    event = service.create_event(
        owner_id=current_user_id,
        title=title,
        start_time=start_time_str,
        end_time=end_time_str,
        description=description,
        location=location,
        participant_ids=participant_ids,
    )

    participants_json = [
        {"user_id": p.user_id, "status": p.status}
        for p in event.participants
    ]

    return {
        "id": event.id,
        "owner_id": event.owner_id,
        "title": event.title,
        "description": event.description,
        "start_time": event.start_time.isoformat(),
        "end_time": event.end_time.isoformat(),
        "location": event.location,
        "participants": participants_json,
    }