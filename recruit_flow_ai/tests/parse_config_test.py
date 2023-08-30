"""
Unit tests for the configuration parsing module.
"""
import unittest
import os
import json
from recruit_flow_ai.parse_config import parse_config, ConfigModel

class TestConfigModel(unittest.TestCase):
    """
    Unit tests for the `ConfigModel` class and the `parse_config` function.
    """
    def setUp(self):
        self.valid_config = {
            "model": "gpt-4",
            "temperature": 0,
            "prompts": { 
                "ai_assistant": {
                    "system": "I am a recruiter specialist in IT service company."
                }
            }
        }
        self.invalid_config = {
            "model": "gpt-4",
            "temperature": 2,  # Invalid temperature
            "prompts": { 
                "ai_assistant": {
                    "system": "I am a recruiter specialist in IT service company."
                }
            }
        }

    def test_parse_config_valid(self):
        with open("test_config.json", "w", encoding='utf-8') as f:
            json.dump(self.valid_config, f)

        config = parse_config("test_config.json")
        self.assertIsInstance(config, ConfigModel)
        os.remove("test_config.json")

    def test_parse_config_invalid(self):
        with open("test_config.json", "w", encoding='utf-8') as f:
            json.dump(self.invalid_config, f)

        with self.assertRaises(ValueError):
            parse_config("test_config.json")
        os.remove("test_config.json")

    def test_parse_config_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            parse_config("nonexistent.json")

if __name__ == "__main__":
    unittest.main()
