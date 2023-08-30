from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pydantic environment settings"""
    api_key: SecretStr

    class Config:
        env_file = ".env"
        env_prefix = "openai_"
        case_sensitive = False

env_settings = Settings()
