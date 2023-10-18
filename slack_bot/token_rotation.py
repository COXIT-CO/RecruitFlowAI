"""
This module contains implementation of app config token rotation logic
"""

import logging
import httpx
from dotenv import find_dotenv, load_dotenv, set_key, dotenv_values
from pydantic import SecretStr
from pydantic_core import ValidationError

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

try:
    from slack_bot.settings import env_settings
except ValidationError:
    env_values = dotenv_values(dotenv_path)
    from slack_bot.settings import Settings
    env_settings = Settings(
            access_token=SecretStr(env_values["SLACK_ACCESS_TOKEN"]),
            signing_secret=SecretStr(env_values["SLACK_SIGNING_SECRET"]),
            config_data_dir=env_values["SLACK_CONFIG_DATA_DIR"],
            app_config_token=SecretStr(env_values["SLACK_APP_CONFIG_TOKEN"]),
            bot_app_id=env_values["SLACK_BOT_APP_ID"],
            refresh_token=SecretStr(env_values["SLACK_REFRESH_TOKEN"])
        )


def get_refresh_token(settings=env_settings):
    """
    Function needed to define a valid refresh token for rotation
    Parameters:
        settings: Settings instance with environment variables, set to env_setting by default
    Returns:
         refresh_token value if configured in .env, otherwise app_config_token
    """
    token = settings.refresh_token.get_secret_value()
    if not token:
        token = settings.app_config_token.get_secret_value()

    return token


def rotate_token(settings=env_settings) -> tuple:
    """
    Token rotation function, which changes values of env values slack_refresh_token and slack_app_config_token as well
    as their values in passed Settings instance
    Parameters:
         settings: Settings instance with environment variables, set to env_setting by default
    Returns:
        Tuple: filled as (new_app_config_token, new_refresh_token) if successful, otherwise empty
    """
    base = "https://slack.com/api/tooling.tokens.rotate"
    data = {"refresh_token": get_refresh_token(settings)}
    response = httpx.post(base, data=data)
    if response.status_code == 200 and response.json()["ok"]:
        response_data = response.json()

        new_refresh_token = response_data["refresh_token"]
        new_config_token = response_data["token"]

        set_key(dotenv_path=dotenv_path, key_to_set="SLACK_REFRESH_TOKEN",
                value_to_set=new_refresh_token)
        set_key(dotenv_path=dotenv_path, key_to_set="SLACK_APP_CONFIG_TOKEN",
                value_to_set=new_config_token)

        settings.refresh_token = SecretStr(new_refresh_token)
        settings.app_config_token = SecretStr(new_config_token)

        return new_config_token, new_refresh_token

    logging.error("Slack Config Token Refreshment Failed; Full response: %s", response.text)
    return ()
