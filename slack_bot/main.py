"""Asyncronious events listener"""
import logging
from fastapi import FastAPI, Request
from slack_bot.bot import app_handler
from slack_bot.bot_setup import update_bot_manifest

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

update_bot_manifest()
fast_app = FastAPI()


@fast_app.post("/slack/events")
async def handle_events(req: Request):
    """Asyncronious events listener of slack bot events"""
    return await app_handler.handle(req)
