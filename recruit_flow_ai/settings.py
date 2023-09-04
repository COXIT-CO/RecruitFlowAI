from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment variables settings"""
    api_key: SecretStr

    class Config:
        env_file = ".env"
        env_prefix = "OPENAI_"
        case_sensitive = False

env_settings = Settings()
