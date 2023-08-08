import ast
import json
import asyncio
import logging
from typing import List
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from prompt import get_prompt_template
from config import openai_api_key, openai_model
from models import Resume, build_resume_model


model = ChatOpenAI(model_name=openai_model, openai_api_key=openai_api_key, verbose=True)
prompt = get_prompt_template()
chain = LLMChain(prompt=prompt, llm=model)

sem = asyncio.Semaphore(3) 

logger = logging.getLogger(__name__)

async def get_clean_text(input_text: str) -> List:
    async with sem:
        response = await chain.arun(input=input_text)
    try:
        correct_sentences = ast.literal_eval(response[18:])
        return correct_sentences
    except:
        logger.error(f"Response format is not correct:\n {response}")
        return None

async def get_clean_resume(resume: dict) -> Resume:
    """ Currently we clean correctly only the summary section.
    Other sections requires different optimised prompts.
    TODO: fix rate limit per minute
    """
    texts = [
        resume['info']['summary'],
        *[e['description'] for e in resume['experiences']],
        *[e['description'] for e in resume['educations']]
    ]
    corrections = await asyncio.gather(*[get_clean_text(text) for text in texts])
    return build_resume_model(resume, corrections)


# TEST
if __name__ == '__main__':
    with open('recruiter_ai/data_examples/parsed_cv_example.json') as cv:
        json_data = json.load(cv)
    sample_event = asyncio.get_event_loop()
    try:
        task_object_loop = sample_event.create_task(get_clean_resume(json_data))
        sample_event.run_until_complete(task_object_loop)
    finally:
        sample_event.close()

    res_obj = task_object_loop.result()
    print(res_obj.dict())