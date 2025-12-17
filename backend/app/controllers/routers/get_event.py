from services.event_service import Events
from controllers.helpers.event_mapper import event_to_response
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from repositories.database import get_db

router = APIRouter()


@router.get("/all_events")
def list_all_events(db: Session = Depends(get_db)):
    service= Events(db)
    events= service.get_all_events()
    return [event_to_response(event) for event in events]


@router.get("/my_events")
def list_events_by_id(db: Session = Depends(get_db), user_id: int | None = Query(None), ):
    service= Events(db)
    events=service.get_events_for_user(user_id=user_id)

    return [event_to_response(event) for event in events]