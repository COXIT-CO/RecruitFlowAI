from pydantic import SecretStr
from pydantic_settings import BaseSettings


class OpenaiSettings(BaseSettings):
    """Environment variables settings"""

    api_key: SecretStr

    class Config:
        env_file = ".env"
        env_prefix = "OPENAI_"
        case_sensitive = False


class MinioSettings(BaseSettings):
    endpoint: str
    access_key: SecretStr
    secret_key: SecretStr
    bucket: str

    class Config:
        env_file = ".env"
        env_prefix = "MINIO_"


class CloudFlareSettings(BaseSettings):
    tunnel_token: SecretStr
    tunnel_url: str

    class Config:
        env_file = ".env"
        env_prefix = "CLOUDFLARE_"
        case_sensitive = False


env_settings = OpenaiSettings()
minio_settings = MinioSettings()
cf_settings = CloudFlareSettings()
