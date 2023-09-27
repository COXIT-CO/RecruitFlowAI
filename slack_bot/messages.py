from pydantic import BaseModel
from typing import List

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


class SlackFileSharedEventModel(BaseModel):
    type: str
    text: str
    files: List
    user: str
    upload: bool
    display_as_bot: bool
    ts: str
    channel: str
    event_ts: str
    channel_type: str
    client_msg_id: str = None
    bot_id: str = None
    thread_ts: str = None

    subtype: str

    def is_from_client(self):
        return self.client_msg_id is not None and self.bot_id is None

