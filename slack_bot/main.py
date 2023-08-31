"""Asyncronious events listener"""
from fastapi import FastAPI, Request
from slack_bot.bot import app_handler
from slack_bot.run_ngrok import setup_ngrok

setup_ngrok()
fast_app = FastAPI()


@fast_app.post("/slack/events")
async def handle_events(req: Request):
    """Asyncronious events listener of slack bot events"""
    return await app_handler.handle(req)
