from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    access_token: SecretStr
    signing_secret: SecretStr

    class Config:
        env_file = '.env'
        env_prefix = "slack_"
        case_sensitive = False