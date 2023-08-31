"""
This module contains the RecruitFlowAI class, which is an AI assistant for the 
RecruitFlow application.

The RecruitFlowAI class provides methods for generating responses based on given 
messages using the OpenAI API.

Example:
    # Create an instance of RecruitFlowAI
    ai = RecruitFlowAI(api_key="YOUR_API_KEY")

    # Generate a response
    response = ai.generate_response(openai_msgs=[
        {"role": "system", "content": "You are a recruitment assistant."},
        {"role": "user", "content": "What questions should I ask during the screening process"}
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

from recruit_flow_ai.parse_config import parse_config, ConfigModel

PROMPTS_CONFIG_PATH = "recruit_flow_ai/prompts_config.json"
ISSUES_REPORT_MSG = "Report this to #recruitflowai_issues channel."

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
        is_valid_api_key_format(api_key: str): Validates the format of an OpenAI API key.

    """
    model = "gpt-3.5-turbo"
    api_key = ""
    system_prompt = "I am helpful recruitment assistant."
    temperature = 0

    def __init__(self, api_key = ""):
        """
        Initializes the RecruitFlowAI object with the provided API key.

        Args:
            api_key (str): The API key for accessing the OpenAI API. If not provided, 
            it will be read from the .env file.

        Raises:
            ValueError: If the API key is not provided or if it is not valid.
        """
        if api_key == "":
            load_dotenv(Path(".env"))
            self.api_key = os.getenv("OPENAI_API_KEY")
            if self.api_key == "":
                raise ValueError("OPENAI_API_KEY is not provided. "/
                                 "Please pass it as an argumant to constructor or add it to .env file")

        else:
            self.api_key = api_key

        if not self.is_valid_api_key_format(self.api_key):
            self.api_key = ""
            raise ValueError("Invalid API key provided!")

        openai.api_key = self.api_key

        config: ConfigModel = parse_config(PROMPTS_CONFIG_PATH)
        if config.temperature:
            if self.is_valid_temperature(temperature=config.temperature):
                logger.error("Temperature is not valid in config. Default will be used.")
            else:
                self.temperature = config.temperature

        if config.model:
            self.model = config.model
            # TODO: add model validation

        if config.prompts["ai_assistant"]:
            self.system_prompt = config.prompts["ai_assistant"].system

    def generate_response(self, openai_msgs: [] ):
        """
        Generates a response based on the given messages.

        Args:
            openai_msgs (list): A list of messages to generate a response from.

        Returns:
            str: The generated response.

        Raises:
            openai.error.Timeout: If the OpenAI API request times out.
            openai.error.APIError: If the OpenAI API returns an error.
            openai.error.APIConnectionError: If the OpenAI API request fails to connect.
            openai.error.InvalidRequestError: If the OpenAI API request is invalid.
            openai.error.AuthenticationError: If the OpenAI API request is not authorized.
            openai.error.PermissionError: If the OpenAI API request is not permitted.
            openai.error.RateLimitError: If the OpenAI API request exceeds the rate limit.
        """
        if self.system_prompt:
            openai_msgs.insert(0, {"role": "system", "content": self.system_prompt})

        error_msg = str()
        response_msg = str()
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=openai_msgs,
                temperature=self.temperature,
                #TODO invetigate if its possible to stream slack message with Slack
                stream=False
            )

            if "choices" in response:
                response_msg = response["choices"][0]["message"]["content"]
            else:
                logger.error("Response is not valid. Correct error handling should be added here")
        except openai.error.Timeout as e:
            #Handle timeout error, e.g. retry or log
            error_msg = "OpenAI API request timed out"
            logger.error("%s: ", error_msg, exc_info=e)
        except openai.error.APIError as e:
            #Handle API error, e.g. retry or log
            error_msg = "OpenAI API returned an API Error"
            logger.error("%s: ", error_msg, exc_info=e)
        except openai.error.APIConnectionError as e:
            #Handle connection error, e.g. check network or log
            error_msg = "OpenAI API request failed to connect"
            logger.error("%s: ", error_msg, exc_info=e)
        except openai.error.InvalidRequestError as e:
            #Handle invalid request error, e.g. validate parameters or log
            error_msg = "OpenAI API request was invalid"
            logger.error("%s: ", error_msg, exc_info=e)
        except openai.error.AuthenticationError as e:
            #Handle authentication error, e.g. check credentials or log
            error_msg = "OpenAI API request was not authorized"
            logger.error("%s: ", error_msg, exc_info=e)
        except openai.error.PermissionError as e:
            #Handle permission error, e.g. check scope or log
            error_msg = "OpenAI API request was not permitted"
            logger.error("%s: ", error_msg, exc_info=e)
        except openai.error.RateLimitError as e:
            #Handle rate limit error, e.g. wait or log
            error_msg = "OpenAI API request exceeded rate limit"
            logger.error("%s: ", error_msg, exc_info=e)

        if response_msg == "":
            response_msg = error_msg + "." + ISSUES_REPORT_MSG

        return response_msg

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
        return bool(isinstance(api_key, str) and re.match(pattern, api_key))

    def is_valid_temperature(self, temperature: float):
        """
        Validates the temperature parameter for controlling the randomness of the generated responses.

        The temperature should be a float between 0 and 1.

        Args:
            temperature (float): The temperature parameter to validate.

        Returns:
            bool: True if the temperature is valid, False otherwise.
        """
        return bool(0 <= temperature <= 1)

