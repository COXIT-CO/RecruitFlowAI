from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment variables settings"""
    access_token: SecretStr
    signing_secret: SecretStr
    app_config_token: SecretStr
    config_data_dir: str
    bot_app_id: str = None

    class Config:
        env_file = ".env"
        env_prefix = "slack_"
        case_sensitive = False

env_settings = Settings()
