"""Asyncronious events listener"""
import logging
from fastapi import FastAPI, Request
from slack_bot.bot import app_handler
from slack_bot.run_ngrok import setup_ngrok

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p"
)

setup_ngrok()
fast_app = FastAPI()


@fast_app.post("/slack/events")
async def handle_events(req: Request):
    """Asyncronious events listener of slack bot events"""
    return await app_handler.handle(req)
