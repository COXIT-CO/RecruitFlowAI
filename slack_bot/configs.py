from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    access_token: SecretStr
    signing_secret: SecretStr
    bot_data_path: str

    class Config:
        env_file = '.env'
        env_prefix = "slack_"
        case_sensitive = False

settings = Settings()