"""
This module contains the RecruitFlowAI class, which is an AI assistant for the RecruitFlow application.

The RecruitFlowAI class provides methods for generating responses based on given messages using the OpenAI API.

Example:
    # Create an instance of RecruitFlowAI
    ai = RecruitFlowAI(api_key="YOUR_API_KEY")

    # Generate a response
    response = ai.generate_response(openai_msgs=[
        {"role": "system", "content": "You are a recruitment assistant."},
        {"role": "user", "content": "What questions should I ask during teh screening process"}
    ])

    # Print the response
    logger.error(response)

"""
import openai

import logging
import re   # used for api key format validation
import os   # used to read OPANAI_API_KEY env variable
from dotenv import load_dotenv
from pathlib import Path

from .parse_config import parse_config, ConfigModel

PROMPTS_CONFIG_PATH = "recruit_flow_ai/prompts_config.json"

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

class RecruitFlowAI:
    """
    AI assistant for the RecruitFlow application.

    Attributes:
        model (str): The name of the GPT model to use.
        api_key (str): The API key for accessing the OpenAI API.
        system_prompt (str): The system prompt to use for generating responses.
        temperature (float): The temperature parameter for controlling the randomness of the generated responses.

    Methods:
        __init__(api_key=""): Initializes the RecruitFlowAI object with the provided API key.
        generate_response(openai_msgs: []): Generates a response based on the given messages.

    """
    model = "gpt-3.5-turbo"
    api_key = ""
    system_prompt = "I am helpful recruitment assistant."
    temperature = 0

    def is_valid_api_key_format(self, api_key: str) -> bool:
        """
        Validates the format of an OpenAI API key.

        The API key should start with "sk-" followed by at least 32 alphanumeric characters.

        Args:
            api_key (str): The API key to validate.

        Returns:
            bool: True if the API key is valid, False otherwise.
        """
        pattern = r"^sk-[a-zA-Z0-9]{32,}$"
        if isinstance(api_key, str) and re.match(pattern, api_key):
            return True
        else:
            return False

    def __init__(self, api_key = ""):
        if api_key == "":
            load_dotenv(Path(".env"))
            self.api_key = os.getenv("OPENAI_API_KEY")
            if self.api_key == "":
                raise ValueError("OPENAI_API_KEY is not provided. "/
                                 "Please pass it as an argumant to constructor or add it to .env file")


        if not self.is_valid_api_key_format(self.api_key):
            raise ValueError("Invalid API key: " + self.api_key)
     
        openai.api_key = self.api_key

        config: ConfigModel = parse_config(PROMPTS_CONFIG_PATH)
        if config.temperature:
            self.temperature = config.temperature
            # TODO: add temperature validation

        if config.model:
            self.model = config.model
            # TODO: add model validation

        if config.prompts["ai_assistant"]:
            self.system_prompt = config.prompts["ai_assistant"].system

    def generate_response(self, openai_msgs: [] ):
        if self.system_prompt:
            openai_msgs.insert(0, {"role": "system", "content": self.system_prompt})

        # Remove duplicated messages, this may happen if slack sends the same bot message as response
        unique_msgs = []
        for msg in openai_msgs:
            if msg not in unique_msgs:
                unique_msgs.append(msg)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=unique_msgs,
                temperature=self.temperature,
                #TODO invetigate if its possible to stream slack message
                stream=False
            )
        except openai.error.Timeout as e:
            #Handle timeout error, e.g. retry or log
            logger.error("OpenAI API request timed out: ", exc_info=e)
            pass
        except openai.error.APIError as e:
            #Handle API error, e.g. retry or log
            logger.error("OpenAI API returned an API Error: ", exc_info=e)
            pass
        except openai.error.APIConnectionError as e:
            #Handle connection error, e.g. check network or log
            logger.error("OpenAI API request failed to connect: ", exc_info=e)
            pass
        except openai.error.InvalidRequestError as e:
            #Handle invalid request error, e.g. validate parameters or log
            logger.error("OpenAI API request was invalid: ", exc_info=e)
            pass
        except openai.error.AuthenticationError as e:
            #Handle authentication error, e.g. check credentials or log
            logger.error("OpenAI API request was not authorized: ", exc_info=e)
            pass
        except openai.error.PermissionError as e:
            #Handle permission error, e.g. check scope or log
            logger.error("OpenAI API request was not permitted: ", exc_info=e)
            pass
        except openai.error.RateLimitError as e:
            #Handle rate limit error, e.g. wait or log
            logger.error("OpenAI API request exceeded rate limit: ", exc_info=e)
            pass


        if "choices" in response:
            response_msg = response["choices"][0]["message"]["content"]
        else:
            # TODO: Add error handling for not success rsponces
            logger.error("Response is not valid. Correct error handling should be added here")

        return response_msg

