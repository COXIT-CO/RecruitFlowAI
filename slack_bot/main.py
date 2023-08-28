"""Asyncronious events listener"""

from fastapi import FastAPI, Request
from slack_bot.bot import app_handler

fast_app = FastAPI()

@fast_app.post("/slack/events")
async def handle_events(req: Request):
    return await app_handler.handle(req)
