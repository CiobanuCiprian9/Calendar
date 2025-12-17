from dotenv import load_dotenv
from fastapi import FastAPI
import os
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from controllers.routers import create_event,get_event,authentification,user_router
from domain import event_handler

def create_app():
    load_dotenv()
    app=FastAPI()
    app.include_router(create_event.router)
    app.include_router(get_event.router)
    app.include_router(user_router.router)

    app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv('SECRET_KEY'),
        same_site="lax",
        https_only=False,
        max_age=60*60*24*7

    )

    fe_origin = os.getenv("FRONTEND_ORIGIN")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[fe_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(authentification.router)
    return app