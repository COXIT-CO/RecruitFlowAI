from pydantic import BaseModel
from typing import List, Optional


class Section(BaseModel):
    input_text: str
    corrected_sentences: list


class Experience(BaseModel):
    title: str
    company: str
    summary: Section
    date_start: str
    date_end: str


class Education(BaseModel):
    title: str
    school: str
    date_start: str
    date_end: str
    summary: Section

    
class Resume(BaseModel):
    full_name: str
    summary: Optional[Section]
    experiences: List[Experience]
    educations: List[Education]
    skills: List[str]


def build_resume_model(resume:dict, corrections:dict) -> Resume:
    data = {
        'full_name': resume['info']['full_name'],
        'summary': {
            'input_text': resume['info']['summary'],
            'corrected_sentences': corrections['summary']
        },
        'experiences': [
                Experience(**exp, 
                           summary=Section(**{
                               'input_text': exp['description'], 
                               'corrected_sentences': corrections['experiences'][i]}
                                )
                           ) for i, exp in enumerate(resume['experiences'])
            ],
        'educations': [
                Education(**ed, 
                           summary=Section(**{
                               'input_text': ed['description'], 
                               'corrected_sentences': corrections['educations'][i]} # todo: include results
                                )
                           ) for i, ed in enumerate(resume['educations'])
            ],
        'skills': [skill['name'] for skill in resume['skills'] if skill['type'] == 'hard']
    }
    return Resume(**data)
    
    

