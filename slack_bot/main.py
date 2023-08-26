import logging
from slack_sdk import WebClient
from fastapi import FastAPI, Depends

from slack_bot.schemas import Command
from slack_bot.command_replies import edit_command, reply_command
from slack_bot.settings import env_settings

logger = logging.getLogger(__name__)
app = FastAPI()
client = WebClient(token=env_settings.access_token.get_secret_value())


@app.post("/process_command")
def process_command(command: Command = Depends()):
    """
        Receive a command from slack bot.
        The command can be sent directly and from the config chat.
        Directly bot can only reply with text
        Via config chat we can edit the bot replies
    """
    if command.text:
        return edit_command(client, command)
    else:
        return reply_command(client, command)
