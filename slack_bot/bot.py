import logging
import os
import urllib.parse
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

from slack_bot.commands import CmdReplyModel
from slack_bot.settings import env_settings
from slack_bot.bot_home_view import get_home_blocks
from slack_bot.messages import SlackMessageEventModel
from slack_bot.utils import (
    convert_slack_msgs_to_openai_msgs,
    AI_PROCESSING_NOTIFICATION_MSG,
)

from recruit_flow_ai import RecruitFlowAI, ResumeHandler

app = AsyncApp(
    token=env_settings.access_token.get_secret_value(),
    signing_secret=env_settings.signing_secret.get_secret_value(),
)
app_handler = AsyncSlackRequestHandler(app)
cmd_replies = CmdReplyModel(
    config_file=os.path.join(env_settings.config_data_dir, "chatcraft_templates.json")
)
ai = RecruitFlowAI()
resume_handler = ResumeHandler()


async def chatcraft_reply(ack, respond, body):
    """General command handler for chatcraft replies"""
    await ack()
    response_text = cmd_replies.get_response_text(
        command_name=body["command"][1:], command_text=body["text"]
    )
    await respond(response_text, unfurl_links=True)
    logging.debug("Chatcraft command %s is handled", body["command"])


async def save_resume_reply(ack, respond, body):
    """General command handler for chatcraft replies"""
    await ack()

    response_text = body["text"]

    # Parse the URL
    url = urllib.parse.urlparse(response_text)

    # Check if the URL is valid
    if not all([url.scheme, url.netloc]):
        response_text = "Invalid URL. Please provide a valid URL."
    else:
        # Check if the file is a PDF
        _, file_extension = os.path.splitext(url.path)
        if file_extension.lower() != ".pdf":
            response_text = "Invalid file type. Please provide a link to a PDF file."
        else:
            response_text = resume_handler.save_resume(url.geturl())
    await respond(response_text, unfurl_links=True)
    logging.debug("save_resume command %s is handled", body["command"])


app.command("/generate_job_description")(chatcraft_reply)
app.command("/create_social_media_post")(chatcraft_reply)
app.command("/match_resumes")(chatcraft_reply)
app.command("/scan_resume")(chatcraft_reply)
app.command("/save_resume")(save_resume_reply)


@app.event("app_home_opened")
async def update_home_tab(client, event):
    """Publish the home view every time the home tab is opened"""
    resp = await client.views_publish(
        user_id=event["user"],
        view={"type": "home", "blocks": get_home_blocks(cmd_replies)},
    )
    if resp["ok"]:
        logging.info("Home tab published successfully")
    else:
        logging.error("Error publishing home tab: %s", resp["error"])


# https://api.slack.com/events/message
@app.event(event={"type": "message", "subtype": "file_share"})
async def reply_in_thread_on_file_share(client, event):
    for file in event["files"]:
        response_text = None
        if "filetype" in file and file["filetype"] != "pdf":
            logging.debug("File type is not supported!")
            response_text = "Invalid file type. Only PDF type is currenty supported."
        elif "url_private_download" in file:
            url = file["url_private_download"]
            logging.debug("Slack file url: {url}")
            s3_url = resume_handler.save_resume(
                url, env_settings.access_token.get_secret_value()
            )
            response_text = s3_url
        else:
            logging.error("Not valid file")
            return

        if response_text:
            post_msg_resp = await client.chat_postMessage(
                channel=event["channel"], text=response_text, thread_ts=event["ts"]
            )
            if post_msg_resp.status_code != 200:
                logging.error(
                    "chat_postMessage request failed, status code=%s",
                    post_msg_resp.status_code,
                )


# https://api.slack.com/events/message
@app.event({"type": "message", "subtype": None})
async def reply_in_thread(client, event):
    message_event = SlackMessageEventModel(**event)
    if message_event.is_from_client():
        logging.debug("Client message received: message=%s", message_event.text)
        thread_ts = (
            message_event.thread_ts if message_event.thread_ts else message_event.ts
        )

        # https://api.slack.com/methods/conversations.replies
        conversation_replies = await client.conversations_replies(
            channel=message_event.channel,
            ts=thread_ts,
        )

        if conversation_replies.status_code != 200:
            logging.error(
                "conversation_replies request failed, status code=%s",
                conversation_replies.status_code,
            )

        # send thsi message just to improve user experience,
        # so if it takes a while to generate response user will know that request i sprocessing
        # ideally message should be streamed to the channel,
        # need to investiagte if possible to do it with Slack
        post_msg_resp = await client.chat_postMessage(
            channel=message_event.channel,
            text=AI_PROCESSING_NOTIFICATION_MSG,
            thread_ts=thread_ts,
        )

        openai_content = ""
        slack_msgs = []
        if "messages" in conversation_replies:
            slack_msgs = conversation_replies["messages"]
            openai_msgs = convert_slack_msgs_to_openai_msgs(slack_msgs)
            openai_content = ai.generate_response(openai_msgs=openai_msgs)
            logging.debug("OpenAI response received: %s", openai_content)
        else:
            logging.debug("No messages found in converstaion_replys response")
            openai_content = (
                "[Server Slack Api Error occured while parsing this thread messages]"
            )

        post_msg_resp = await client.chat_postMessage(
            channel=message_event.channel, text=openai_content, thread_ts=thread_ts
        )

        if post_msg_resp.status_code != 200:
            logging.error(
                "chat_postMessage request failed, status code=%s",
                post_msg_resp.status_code,
            )
    else:
        logging.debug("Not a user message. Should be Bot message.")
