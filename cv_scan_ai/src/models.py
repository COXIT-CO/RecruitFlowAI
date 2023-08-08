from pydantic import BaseModel
from typing import List, Union
from tools.text_reviewer import get_clean_text

class Section(BaseModel):
    input_text: str
    corrected_sentences: list

class CorrectSummaryModel(BaseModel):
    summary: Union[Section, str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_text = None
        if kwargs.get('summary', None):
            input_text = kwargs['summary']
        elif kwargs.get('description', None):
            input_text = kwargs['description']
        if input_text:
            self.summary = Section(**{
                'input_text': input_text,
                'corrected_sentences': get_clean_text(input_text)
            })

class Experience(CorrectSummaryModel):
    title: str
    company: str   
    date_start: str
    date_end: str


class Education(CorrectSummaryModel):
    title: str
    school: str
    date_start: str
    date_end: str


class Skill(BaseModel):
    name: str
    type: str


class Resume(CorrectSummaryModel):
    full_name: str
    experiences: List[Experience]
    educations: List[Education]
    skills: List[Skill]
