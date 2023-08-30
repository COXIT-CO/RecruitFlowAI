""" Application entry point """
from typing import Tuple, Any
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

from pdfminer.high_level import extract_text
from kor import from_pydantic, create_extraction_chain

from settings import env_settings
from models import Candidate
from examples import read_examples


llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    max_tokens=2000,
    openai_api_key=env_settings.api_key.get_secret_value()
)

schema, validator = from_pydantic(
    Candidate,
    description="""Extract information about job caondidate from his resume including email,
full name, summary, all mentioned skills, education and experience""",
    examples=read_examples()
)

chain = create_extraction_chain(llm,
                                schema,
                                validator=validator,
                                encoder_or_encoder_class="json",
                                input_formatter="triple_quotes")

def parse_resume(path: str)->Candidate:
    cv_text = extract_text(path)
    return chain.run(cv_text)["validated_data"]


def get_prompt()->str:
    return chain.prompt.format_prompt(text="[resume text]").to_string()


def parse_resume_with_metrics(path: str)->Tuple[Candidate, Any]:
    cv_text = extract_text(path)
    with get_openai_callback() as metrics:
        return chain.run(cv_text)["validated_data"], metrics
