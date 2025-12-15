from fastapi import APIRouter, HTTPException,Request,Depends,status
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from repositories.database import get_db

router=APIRouter()

@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    first_name = body.get("first_name")
    last_name = body.get("last_name")
    email = body.get("email")
    password = body.get("password")

    if not first_name or not last_name or not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="first_name, last_name, email, password are missing!",
        )

    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already used!",
        )

    last_id = db.query(func.max(models.User.id)).scalar() or 0
    new_id = last_id + 1

    user = models.User(
        id=new_id,
        first_name=first_name,
        middle_name=None,
        last_name=last_name,
        email=email,
        password_hash=password,
        timezone="Europe/Bucharest",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email and password are mandatory!",
        )

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or user.password_hash!=password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or/and password are incorrect!",
        )

    return {
        "user_id": user.id,
        "email": user.email,
        "message": "login ok",
    }