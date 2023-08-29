import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

from slack_bot.reply_models import CmdReplyModel
from slack_bot.settings import env_settings

logging.basicConfig(level=logging.DEBUG)
app = AsyncApp(
    token=env_settings.access_token.get_secret_value(),
    signing_secret=env_settings.signing_secret.get_secret_value()
)
app_handler = AsyncSlackRequestHandler(app)
cmd_replies = CmdReplyModel(config_file=env_settings.config_data_dir+"/chatcraft_templates.json")


async def chatcraft_reply(ack, respond, body):
    """General command handler for chatcraft replies"""
    await ack()
    response_text = cmd_replies.get_response_text(command_name=body["command"][1:],
                                                  command_text=body["text"])
    await respond(response_text, unfurl_links=True)


app.command("/generate_job_description")(chatcraft_reply)
app.command("/create_social_media_post")(chatcraft_reply)
app.command("/match_resumes")(chatcraft_reply)
app.command("/scan_resume")(chatcraft_reply)


@app.event("app_home_opened")
async def update_home_tab(client, event, logger):
    view_model = {
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome home, <@" + event["user"] + "> :house:*"
                        }
                    }
                ]
            }
    view_model["blocks"].append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Follow the link below to process the candidate:",
            "emoji": True
        }
    })
    for text in cmd_replies.iter_chatcraft_replies():
        view_model["blocks"].append({
            "type": "divider",
        })
        view_model["blocks"].append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        })

    view_model["blocks"].append({
        "type": "divider",
    })
    view_model["blocks"].append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "Current configuration file:",
            "emoji": True
        }
    })
    view_model["blocks"].append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "```\n" + cmd_replies.get_config_json() + "```"
        }
    })
    
    try:
        await client.views_publish(
            user_id=event["user"],
            view= view_model
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
