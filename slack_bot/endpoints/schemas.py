"""Model of incoming request from slack slash commands"""
from urllib.parse import parse_qsl
from typing import List, Any, Optional
from pydantic import BaseModel
from fastapi import Depends, Request

async def with_body(request: Request) -> bytes:
    """Return request body.

    Per design, a route cannot depend on a form field and consume body because
    dependencies resolution consumes body.
    Therefore, this is not using `fastapi.Form` to extract form data parameters.
    """
    return await request.body()


def with_form_data(body: bytes = Depends(with_body)) -> dict:
    return dict(parse_qsl(body.decode()))


class Command(BaseModel):
    """Model of incoming request from slack slash commands """
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

    def __init__(self, form_data: dict = Depends(with_form_data)):
        super().__init__(**form_data)


class SlackMessageEventModel(BaseModel):
    """ https://api.slack.com/events/message """
    client_msg_id: Optional[str] = None
    bot_id: Optional[str] = None
    type: str
    text: str
    user: str
    ts: str
    blocks: List
    team: str
    channel: str
    event_ts: str
    thread_ts: str = None
    channel_type: str


class SlackEventModel(BaseModel):
    """ https://api.slack.com/events/message """
    token: str
    team_id: str = None
    context_team_id: str = None
    context_enterprise_id: Any = None
    api_app_id: str = None
    event: SlackMessageEventModel = None
    type: str
    event_id: str = None
    event_time: int = None
    authorizations: List = None
    is_ext_shared_channel: bool = None
    event_context: str = None
    challenge: str = None
