import os

from fastapi import APIRouter, HTTPException,Request,Depends,status
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models
from auth.google_oauth import oauth
from repositories.database import get_db

router=APIRouter(prefix="/auth")

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

#google auth
def create_token_for_user(user: models.User) -> str:
    import uuid
    return str(uuid.uuid4())

@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    try:
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        print("Google login error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Google login failed: {e}",
        )

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google auth failed",
        )

    userinfo = token.get("userinfo")
    if not userinfo:
        userinfo = await oauth.google.parse_id_token(request, token)

    email = userinfo.get("email")
    first_name = userinfo.get("given_name", "")
    last_name = userinfo.get("family_name", "")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Google did not return email",
        )

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            first_name=first_name or "Google",
            middle_name=None,
            last_name=last_name or "",
            email=email,
            password_hash="",
            timezone="Europe/Bucharest",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_token_for_user(user)


    redirect_url = f"{FRONTEND_ORIGIN}/auth/google-success?user_id={user.id}&access_token={access_token}"
    return RedirectResponse(url=redirect_url)