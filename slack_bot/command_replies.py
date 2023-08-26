import logging
from fastapi import Response

from slack_sdk import WebClient
from slack_sdk.errors import SlackClientError

from slack_bot.settings import env_settings
from slack_bot.schemas import Command, CommandReplies
from slack_bot.utils import is_chatcraft_url

logger = logging.getLogger(__name__)
replies = CommandReplies(file_path=env_settings.bot_data_path)


def reply_command(client: WebClient, command: Command):
    command_name = command.command[1:]
    if command_name in replies.model_fields:
        answear = getattr(replies, command_name)
    else:
        logger.error("Unknown command was send: %s", command_name)
        answear = f"Unknown command: {command_name}"
    try:
        resp = client.chat_postMessage(
            channel=command.channel_id,
            text=answear.title,
            unfurl_links=False,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": answear.get_markdwn(),
                    }
                }
            ],
        )
        return Response(status_code=resp.status_code)
    except SlackClientError as e:
        logger.error("Slack client error sending reply to command %s: \n", command.command, exc_info=e)
        return Response(status_code=500)


def edit_command(client: WebClient, command: Command):
    cmd_reply = getattr(replies, command.command[1:])
    if is_chatcraft_url(command.text):
        field_name = "url"
        old_value = cmd_reply.url
        cmd_reply.url = command.text
    elif "hint" in command.text[:10].lower():
        field_name = "hint"
        old_value = cmd_reply.hint
        cmd_reply.hint = command.text.lstrip("*Hhint: ")
    else:
        resp = client.chat_postMessage(
            channel=command.channel_id,
            text="I can't edit this command with provided data. "\
            "Please provide chatcraft url or the text starting with 'Hint:' keyword"
        )
        return Response(status_code=200)
    replies.save_model()
    try:
        resp = client.chat_postMessage(
            channel=command.channel_id,
            text=f"{command.command} reply changed the {field_name} from {old_value} to {command.text}"
        )
        return Response(status_code=resp.status_code)
    except SlackClientError as e:
        logger.error("Slack client error sending reply to command %s: \n", command.command, exc_info=e)
        return Response(status_code=500)
