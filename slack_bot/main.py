"""Application entry point"""
from fastapi import FastAPI
from .endpoints import api_router

app = FastAPI()
app.include_router(api_router)

