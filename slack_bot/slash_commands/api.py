import logging
import slack_sdk
from fastapi import APIRouter, Depends, Response

from slack_bot.slash_commands.schemas import Command
from slack_bot.slash_commands.answears import get_answear
from slack_bot.settings import env_settings

logger = logging.getLogger(__name__)
router = APIRouter()
client = slack_sdk.WebClient(token=env_settings.access_token.get_secret_value())


@router.post('/process_command')
def process_command(command: Command = Depends()):
    text = get_answear(command.command[1:])
    try:
        client.chat_postMessage(channel=command.channel_id,
                        text="",
                        unfurl_links=False,
                        blocks=[
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": text
                                }
                            }
                        ],
                    )
    except Exception as e:
        logger.error(f"Error in processing command '{command.command}' : ", exc_info=e)
        return Response(status_code=500)
    return Response(status_code=200)
