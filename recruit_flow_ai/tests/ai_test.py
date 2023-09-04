"""
This module contains unit tests for the RecruitFlowAI class. 
"""
import unittest
from unittest.mock import patch
from recruit_flow_ai import RecruitFlowAI
import openai

class TestRecruitFlowAI(unittest.TestCase):
    """
    Unit test class for testing the RecruitFlowAI class.
    """
    def setUp(self):
        self.ai = RecruitFlowAI(api_key="sk-test12345678901234567890123456789012")

    def test_is_valid_api_key_format(self):
        self.assertTrue(self.ai.is_valid_api_key_format("sk-test12345678901234567890123456789012"))
        self.assertFalse(self.ai.is_valid_api_key_format("invalid_key"))

    def test_is_valid_temperature(self):
        self.assertTrue(self.ai.is_valid_temperature(0.5))
        self.assertFalse(self.ai.is_valid_temperature(1.5))

    @patch("openai.ChatCompletion.create")
    def test_generate_response(self, mock_create):
        mock_create.return_value = {
        "id": "chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve",
        "object": "chat.completion",
        "created": 1677649420,
        "model": "gpt-3.5-turbo",
        "usage": {"prompt_tokens": 56, "completion_tokens": 31, "total_tokens": 87},
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Test response"
                },
                "finish_reason": "stop",
                "index": 0
            }
        ]
        }
        response = self.ai.generate_response(openai_msgs=[{"role": "user", "content": "Test message"}])
        self.assertEqual(response, "Test response")

    @patch("openai.ChatCompletion.create")
    def test_generate_response_error(self, mock_create):
        mock_create.side_effect = openai.error.APIError("Test error")
        response = self.ai.generate_response(openai_msgs=[{"role": "user", "content": "Test message"}])
        self.assertIn("Report this to #recruitflowai_issues channel.", response)

if __name__ == "__main__":
    unittest.main()
