"""
This module contains unit tests for the slack_bot.endpoints.api module.

These tests use the unittest.mock library to replace the actual client with a
mock object, allowing us to simulate various scenarios and check how the
functions under test react.
"""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock
from slack_bot.endpoints.api import convert_slack_msgs_to_openai_msgs, handle_message_events

class TestFunctions(IsolatedAsyncioTestCase):
    """
    This class contains unit tests for the functions in the slack_bot.endpoints.api module.
    """
    def test_convert_slack_msgs_to_openai_msgs(self):
        slack_messages = [
            {"client_msg_id": "1", "text": "Hello"},
            {"bot_id": "2", "text": "Hi"},
            {"other_id": "3", "text": "Hey"},
        ]
        expected_result = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        result = convert_slack_msgs_to_openai_msgs(slack_messages)
        self.assertEqual(result, expected_result)

    @patch("slack_bot.endpoints.api.client")
    async def test_handle_message_events(self, mock_client):
        request_body_json = {
            "token": "xoxb-1234567890-abcdefgh",
            "team_id": "T01",
            "context_team_id": "T01",
            "context_enterprise_id": "E01",
            "api_app_id": "A01",
            "event": {
                "client_msg_id": "1234567890.123456",
                "type": "message",
                "text": "Hello, world!",
                "user": "U01",
                "ts": "1615868277.000200",
                "blocks": [],
                "team": "T01",
                "channel": "C01",
                "event_ts": "1615868277.000200",
                "thread_ts": "1615868277.000200",
                "channel_type": "channel"
            },
            "type": "event_callback",
            "event_id": "Ev01",
            "event_time": 1615868277,
            "authorizations": [],
            "is_ext_shared_channel": "false",
            "event_context": "EC01"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.chat_postMessage.return_value = mock_response
        await handle_message_events(request_body_json)
        mock_client.chat_postMessage.assert_called_once()

    @patch("slack_bot.endpoints.api.client")
    async def test_handle_message_events_bot_message(self, mock_client):
        request_body_json = {
            "token": "xoxb-1234567890-abcdefgh",
            "team_id": "T01",
            "context_team_id": "T01",
            "context_enterprise_id": "E01",
            "api_app_id": "A01",
            "event": {
                "bot_id": "1234567890.123456",
                "type": "message",
                "text": "Hello, world!",
                "user": "U01",
                "ts": "1615868277.000200",
                "blocks": [],
                "team": "T01",
                "channel": "C01",
                "event_ts": "1615868277.000200",
                "thread_ts": "1615868277.000200",
                "channel_type": "channel"
            },
            "type": "event_callback",
            "event_id": "Ev01",
            "event_time": 1615868277,
            "authorizations": [],
            "is_ext_shared_channel": "false",
            "event_context": "EC01"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.chat_postMessage.return_value = mock_response
        await handle_message_events(request_body_json)
        mock_client.chat_postMessage.assert_not_called()

    @patch("slack_bot.endpoints.api.client")
    async def test_handle_message_events_invalid_json(self, mock_client):
        request_body_json = {
            "invalid_key": "invalid_value"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.chat_postMessage.return_value = mock_response
        await handle_message_events(request_body_json)
        mock_client.chat_postMessage.assert_not_called()
