from dotenv import load_dotenv
from fastapi import FastAPI
from controllers.routers import test

def create_app():
    load_dotenv()
    app=FastAPI()
    app.include_router(test.router)

    return app