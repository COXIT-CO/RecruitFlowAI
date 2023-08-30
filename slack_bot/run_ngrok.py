import os
import sys
import json
import logging
from pyngrok import ngrok
from slack_sdk import WebClient
from slack_bot.settings import env_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_bot_manifest(public_url:str):
    """Updates bot manifest with current ngrok tunnel url"""
    client = WebClient(token=env_settings.app_config_token.get_secret_value())
    with open (os.path.join(env_settings.config_data_dir, "manifest.json"), "r") as file:
        manifest_string = file.read().replace("{$bot_base_url}", public_url)
        manifest_json = json.loads(manifest_string)
    response = client.api_call(
        api_method="apps.manifest.update",
        json={
            "app_id": env_settings.bot_app_id,
            "manifest": manifest_json
        }
    )
    if response["ok"]:
        logger.info("Manifest updated successfully")
    else:
        logger.error("Error updating manifest: %s", response["error"])


def setup_ngrok():
    """Create new ngrok tunnel and updates the manifest file"""
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
    public_url = ngrok.connect(port).public_url
    logger.info("Running ngrok tunnel %s -> http://localhost:%s", public_url, port)
    update_bot_manifest(public_url)
