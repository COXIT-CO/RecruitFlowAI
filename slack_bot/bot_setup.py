import os
import json
import logging
from slack_bolt import App
from recruit_flow_ai.settings import cf_settings
from slack_bot.settings import env_settings
from slack_bot.token_rotation import rotate_token


rotate_token()

app = App(token=env_settings.app_config_token.get_secret_value())


def update_bot_manifest():
    """Updates bot manifest with current cloudflare tunnel url"""
    public_url = cf_settings.tunnel_url

    with open(os.path.join(env_settings.config_data_dir, "manifest.json"), "r") as file:
        manifest_string = file.read().replace("{$bot_base_url}", public_url)
        manifest_json = json.loads(manifest_string)
    response = app.client.api_call(
        api_method="apps.manifest.update",
        json={"app_id": env_settings.bot_app_id, "manifest": manifest_json},
    )
    if response["ok"]:
        logging.info("Manifest updated successfully")
    else:
        logging.error("Error updating manifest: %s", response["error"])
