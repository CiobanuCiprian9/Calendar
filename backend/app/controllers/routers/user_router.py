from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from repositories.database import get_db
from services.user_service import UserService

router = APIRouter()

@router.get("/search")
def search_users(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):

    service = UserService(db)
    users = service.search_users(q)

    return [
        {
            "id": u.id,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
        }
        for u in users
    ]