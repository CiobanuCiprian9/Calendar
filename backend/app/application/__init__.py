from dotenv import load_dotenv
from fastapi import FastAPI
from controllers.routers import create_event

def create_app():
    load_dotenv()
    app=FastAPI()
    app.include_router(create_event.router)

    return app