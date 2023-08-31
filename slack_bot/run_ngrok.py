import os
import sys
import json
import logging
from pyngrok import ngrok, conf
from pyngrok.exception import PyngrokNgrokError
from slack_sdk import WebClient
from slack_bot.settings import env_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_event_callback(log):
    logger.debug("Ngrok log: %s", log)

conf.get_default().log_event_callback = log_event_callback

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

def get_port(default_port=8000):
    # Check if "--port" is in the command line arguments
    if "--port" in sys.argv:
        # Find the index of "--port"
        port_index = sys.argv.index("--port")

        # Check if there is another argument after "--port"
        if port_index + 1 < len(sys.argv):
            # Get the argument after "--port"
            port_argument = sys.argv[port_index + 1]

            # Try to convert the argument to an integer
            try:
                return int(port_argument)
            except ValueError:
                logging.error("Invalid port number '%s'. Using default port %s.", port_argument, default_port)
        else:
            logging.error("'--port' argument provided but no port number specified. Using default port %s."
                          , default_port)
    else:
        logging.info("'--port' argument not provided. Using default port %s.", default_port)

    return default_port


def setup_ngrok():
    """Create new ngrok tunnel and updates the manifest file"""
    port = get_port()
    try:
        http_tunnel = ngrok.connect(port)
        public_url = http_tunnel.public_url

        logger.info("Running ngrok tunnel %s -> http://localhost:%s", public_url, port)
        update_bot_manifest(public_url)
    except PyngrokNgrokError as e:
        logger.error("Ngrok exception: ", exec=e)
