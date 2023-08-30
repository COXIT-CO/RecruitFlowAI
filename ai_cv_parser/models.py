from typing import List
from pydantic.v1 import BaseModel, Field


class Candidate(BaseModel):
    """
    Pydantic model that describes the data expected to parse from the CV.
    Field descriptions will be used for OpenAI prompt
    """
    email: str = Field(description="The email of a job candidate")
    full_name: str = Field(description="The full name of a job candidate")
    summary: str = Field(
        description="The summary (also named as objective or profile) section of the resume")
    skills: List[str] = Field(
        description="A list of technical skills and technologies and tools that were mentioned in the resume")
    education: List[str] = Field(
        description="A list of education titles found in the resume including the degrees and universities")
    experience: int = Field(
        description="A number of years of career based on previous experience, considering that today is 2023")
