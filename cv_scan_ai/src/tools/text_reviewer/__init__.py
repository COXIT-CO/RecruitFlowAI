import ast
import json
import logging
from typing import List
from langchain import LLMChain
from langchain.llms.base import create_base_retry_decorator
from langchain.chat_models import ChatOpenAI
from openai.error import RateLimitError
from .prompt import get_prompt_template
from .config import openai_api_key, openai_model


model = ChatOpenAI(model_name=openai_model, openai_api_key=openai_api_key)
prompt = get_prompt_template()
chain = LLMChain(prompt=prompt, llm=model)
retry_decorator = create_base_retry_decorator(error_types=[RateLimitError])

logger = logging.getLogger(__name__)

@retry_decorator
def get_clean_text(input_text: str) -> List:
    response = chain.run(input=input_text)
    try:
        correct_sentences = ast.literal_eval('['+response.split('[', 1)[1])
        return correct_sentences
    except:
        logger.error(f"Response format is not correct:\n {response}")
        return None
