import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

from slack_bot.commands import CmdReplyModel
from slack_bot.settings import env_settings
from slack_bot.bot_home_view import get_home_blocks
from slack_bot.messages import SlackMessageEventModel
from slack_bot.utils import convert_slack_msgs_to_openai_msgs, AI_PROCESSING_NOTIFICATION_MSG

from recruit_flow_ai import RecruitFlowAI

app = AsyncApp(
    token=env_settings.access_token.get_secret_value(),
    signing_secret=env_settings.signing_secret.get_secret_value()
)
app_handler = AsyncSlackRequestHandler(app)
cmd_replies = CmdReplyModel(config_file=os.path.join(env_settings.config_data_dir,"chatcraft_templates.json"))
ai = RecruitFlowAI()

async def chatcraft_reply(ack, respond, body, logger):
    """General command handler for chatcraft replies"""
    await ack()
    response_text = cmd_replies.get_response_text(command_name=body["command"][1:],
                                                  command_text=body["text"])
    await respond(response_text, unfurl_links=True)
    logger.debug("Chatcraft command %s is handled", body["command"])


app.command("/generate_job_description")(chatcraft_reply)
app.command("/create_social_media_post")(chatcraft_reply)
app.command("/match_resumes")(chatcraft_reply)
app.command("/scan_resume")(chatcraft_reply)


@app.event("app_home_opened")
async def update_home_tab(client, event, logger):
    """Publish the home view every time the home tab is opened"""
    resp = await client.views_publish(
        user_id=event["user"],
        view= {
            "type": "home",
            "blocks": get_home_blocks(cmd_replies)
        }
    )
    if resp["ok"]:
        logger.info("Home tab published successfully")
    else:
        logger.error("Error publishing home tab: %s", resp["error"])

# https://api.slack.com/events/message
@app.event({"type": "message", "subtype": None})
async def reply_in_thread(client, event, logger):
    message_event = SlackMessageEventModel(**event)
    if message_event.is_from_client():
        thread_ts = message_event.thread_ts if message_event.thread_ts else message_event.ts

        # https://api.slack.com/methods/conversations.replies
        conversation_replies = await client.conversations_replies(
            channel=message_event.channel,
            ts = thread_ts,
        )

        if conversation_replies.status_code != 200:
            logger.error("conversation_replies request failed, status code=%s", conversation_replies.status_code)

        # send thsi message just to improve user experience,
        # so if it takes a while to generate response user will know that request i sprocessing
        # ideally message should be streamed to the channel,
        # need to investiagte if possible to do it with Slack
        post_msg_resp = await client.chat_postMessage(channel=message_event.channel,
            text=AI_PROCESSING_NOTIFICATION_MSG,
            thread_ts=thread_ts
        )

        openai_content = ""
        slack_msgs = []
        if "messages" in conversation_replies:
            slack_msgs = conversation_replies["messages"]
            openai_msgs = convert_slack_msgs_to_openai_msgs(slack_msgs)
            openai_content = ai.generate_response(openai_msgs=openai_msgs)
            logger.debug("OpenAI response received: %s", openai_content)
        else:
            logger.debug("No messages found in converstaion_replys response")
            openai_content = "[Server Slack Api Error occured while parsing this thread messages]"

        post_msg_resp = await client.chat_postMessage(channel=message_event.channel,
            text=openai_content,
            thread_ts=thread_ts
        )

        if post_msg_resp.status_code != 200:
            logger.error("chat_postMessage request failed, status code=%s", post_msg_resp.status_code)
    else:
        logger.debug("Not a user message. Should be Bot message.")
