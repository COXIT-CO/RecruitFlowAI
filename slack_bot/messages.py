"""
This module defines the data models for Slack events, specifically message events
and file shared events. These models are used to parse and validate the data 
received from Slack's Event API.

Classes:
    SlackMessageEventModel: Data model for message events from Slack.
    SlackFileSharedEventModel: Data model for file shared events from Slack.
"""
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
    """ https://api.slack.com/events/message/file_share """
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

