from dotenv import load_dotenv
from fastapi import FastAPI
import os
from starlette.middleware.cors import CORSMiddleware
from controllers.routers import create_event,get_event,authentification


def create_app():
    load_dotenv()
    app=FastAPI()
    app.include_router(create_event.router)
    app.include_router(get_event.router)
    app.include_router(authentification.router)

    fe_origin = os.getenv("FRONTEND_ORIGIN")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[fe_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return app