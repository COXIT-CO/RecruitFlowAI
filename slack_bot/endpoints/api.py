"""Enpoint to process slash commands"""
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from fastapi import APIRouter, Depends, Response, Request, BackgroundTasks
from typing import Any

from slack_bot.endpoints.schemas import Command, SlackEventModel
from slack_bot.endpoints.answears import get_answear
from slack_bot.settings import env_settings
from recruit_flow_ai import RecruitFlowAI

# TODO: make logging configurable in one place to be common for all modules 
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

router = APIRouter()
client = WebClient(token=env_settings.access_token.get_secret_value())
ai = RecruitFlowAI()

@router.post("/process_command")
def process_command(command: Command = Depends()):
    text = get_answear(command.command[1:])
    try:
        # TODO: beteter to make this request asynchronously?
        resp = client.chat_postMessage(channel=command.channel_id,
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
        # TODO: if the command is /ai_assistant then call message handler
    except SlackApiError as e:
        logger.error("Error in processing command '%s': ", command.command, exc_info=e)
    return Response(status_code=resp.status_code)

@router.post("/message")
async def process_message(request: Request, background_tasks: BackgroundTasks) -> Any:
    request_body_json = await request.json()
    background_tasks.add_task(handle_message_events, request_body_json)
    return Response(status_code=200)

def convert_slack_msgs_to_openai_msgs(slack_messages):
    openai_messages = []
    for message in slack_messages:
        if "client_msg_id" in message:
            role = "user"
        elif "bot_id" in message:
            role = "assistant"
        else:
            continue
        content = message["text"]
        openai_messages.append({"role": role, "content": content})
    return openai_messages

async def handle_message_events(request_body_json):

    try:
        logger.debug("Message received: %s", request_body_json)
        slack_message = SlackEventModel(request_body_json)

        # parse only user messages (indicated with client_msg_id field)
        # no need to react on bot messages
        if slack_message.event.client_msg_id:
            logger.debug("Message identified as Client message: message_text=%s", 
                         slack_message.event.text)
            if len(slack_message.event.text) == 0:
                # why would we handle empty messages from the user, skip it
                logger.debug("Empty messages received. Skipping it.")
                return Response(status_code=200)

            # Use "ts" or "thread_ts" as thread identifier
            ts = slack_message.event.ts
            if slack_message.event.thread_ts is not None:
                logger.debug("Message was sent as thread reply")
                ts = slack_message.event.thread_ts

            # https://api.slack.com/methods/conversations.replies
            conversation_replies = client.conversations_replies(
                channel=slack_message.event.channel,
                ts = ts,
            )

            openai_content = ""
            if "messages" in conversation_replies:
                slack_msgs = conversation_replies["messages"]
                openai_msgs = convert_slack_msgs_to_openai_msgs(slack_messages=slack_msgs)
                openai_content = ai.generate_response(openai_msgs=openai_msgs)
                logger.debug("OpenAI response received: %s", openai_content)
            else:
                logger.debug("No messages found in converstaion_replys response")
                openai_content = "[Server Slack Api Error occured while parsing this thread messages]"

            post_msg_resp = client.chat_postMessage(channel=slack_message.event.channel,
                text="",
                thread_ts=ts,
                unfurl_links=False,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": openai_content
                        }
                    }
                ],
            )

            if post_msg_resp.status_code != 200:
                logger.error("chat_postMessage request failed, status code=%s", post_msg_resp.status_code)
        else:
            logger.debug("Not a user message. Should be Bot message.")
    except SlackApiError as e:
        logger.error("Error in processing message request: ", exc_info=e)


