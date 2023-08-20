import slack_sdk
from hmac import HMAC
from time import time
from hashlib import sha256
from urllib.parse import parse_qsl
from pydantic import BaseModel, ValidationError
from fastapi import APIRouter, Depends, Response, Header, HTTPException, Request

from slack_bot.slash_commands.answears import get_answear
from slack_bot.settings import Settings, env_settings

router = APIRouter()
client = slack_sdk.WebClient(token=env_settings.access_token.get_secret_value())


def with_valid_timestamp(x_slack_request_timestamp: int = Header(...)) -> int:
    now = time()
    more_than_thirty_seconds = now - x_slack_request_timestamp > 30
    if more_than_thirty_seconds:
        raise HTTPException(400, "Invalid timestamp")
    return x_slack_request_timestamp


async def with_body(request: Request) -> bytes:
    """Return request body.

    Per design, a route cannot depend on a form field and consume body because
    dependencies resolution consumes body.
    Therefore, this is not using `fastapi.Form` to extract form data parameters.
    """
    return await request.body()


def with_form_data(body: bytes = Depends(with_body)) -> dict:
    return dict(parse_qsl(body.decode()))


def check_signature(secret: str, timestamp: int, signature: str, body: bytes) -> bool:
    """Return True if signature is valid and False if not."""
    signature_message = f"v0:{timestamp}:{body.decode()}"
    local_hash = HMAC(
        secret.encode(), signature_message.encode(), sha256).hexdigest()
    local_signature = f"v0={local_hash}"
    return local_signature == signature


def with_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as error:
        raise HTTPException(500) from error


def with_valid_signature(
    body: bytes = Depends(with_body),
    settings: Settings = Depends(with_settings),
    timestamp: int = Depends(with_valid_timestamp),
    signature: str = Header(..., alias="X-Slack-Signature"),
) -> str:
    secret = settings.signing_secret.get_secret_value()
    if check_signature(secret, timestamp, signature, body) is False:
        raise HTTPException(403, "invalid signature")
    return signature


class Command(BaseModel):
    token: str
    team_id: str
    team_domain: str
    channel_id: str
    channel_name: str
    user_id: str
    user_name: str
    command: str
    response_url: str
    trigger_id: str
    api_app_id: str
    text: str = None
    enterprise_id: str = None
    enterprise_name: str = None

    def __init__(
        self,
        form_data: dict = Depends(with_form_data),
        signature=Depends(with_valid_signature),
    ):
        super().__init__(**form_data)


@router.post('/process_command')
def process_command(command: Command = Depends()):
    text = get_answear(command.command[1:])
    client.chat_postMessage(channel=command.channel_id,
                            text="",
                            unfurl_links=False,
                            blocks=[
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": text
                                    }
                                }
                            ],
                        )
    return Response(status_code=200)
