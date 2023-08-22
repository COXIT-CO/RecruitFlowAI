"""Application entry point"""
from fastapi import FastAPI
from .slash_commands import slash_commands_router

app = FastAPI()
app.include_router(slash_commands_router)
