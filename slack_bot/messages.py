from pydantic import BaseModel
from typing import List, Any, Optional

class SlackMessageEventModel(BaseModel):
    """ https://api.slack.com/events/message """
    client_msg_id: str = None
    bot_id: str = None
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

    def is_from_client(self):
        return self.client_msg_id is not None and self.bot_id is None


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

