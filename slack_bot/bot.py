from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

from slack_bot.commands import CmdReplyModel
from slack_bot.settings import env_settings
from slack_bot.app_home_view import get_home_blocks


app = AsyncApp(
    token=env_settings.access_token.get_secret_value(),
    signing_secret=env_settings.signing_secret.get_secret_value()
)
app_handler = AsyncSlackRequestHandler(app)
cmd_replies = CmdReplyModel(config_file=env_settings.config_data_dir+"chatcraft_templates.json")


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

