from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

template = """
You are a recruiter that have to validate the text of the CV send for the customer. 
You have to divide the text into the sentences and then:
- fix all spelling mistakes
- refrase sentences using correct grammar
- remove the punctuation mistakes, like missing or redandunt comma or period
- summurize the text if the information is duplicated
Correct senteces should be represented as python list of strings. If no changes applied to the sentence - put "None" instead.
Input text: {input}
Correct sentences: {correct_sentences}
"""

examples = [
    {
        "input": """
My name is Sviatoslav, I've been working with Data scientist and machine learning for 4+ years.  I've taken part in machine
learning and computer vision research and development. I developed architecture approaches wich halped to calculate neural
network post-processing for car collision avoidance neural network computer vision system for segmentation of pixel of
agricultural fields their boundary and values of crops in each piccel regions. Theseus challenges have gave me understanding of
geometrical math, statistics.
        """,
        "correct_sentences": """
[
    "My name is Sviatoslav, I've been working as data scientist and machine learning expert for 4+ years.",
    None,
    I developed architecture approaches wich halped to calculate neural network post-processing for car collision avoidance, neural network computer vision system for segmentation of pixel of agricultural fields their boundary and values of crops in each pixel regions."
    "Theseus challenges gave me understanding of geometrical math and statistics."
]""",
    },
    {
        "input": """
Results-driven Machine Learning Engineer with a strong background in software engineering, data analysis, and machine
learning, predominantly focused on computer vision. Skilled in designing scalable solutions, extracting insights from complex
datasets, and applying machine learning algorithms to solve real-world problems.
        """,
        "correct_sentences": """
[
    "Results-driven Machine Learning Engineer with a strong background in software engineering, data analysis and machine learning, predominantly focused on computer vision.",
    "Skilled in designing scalable solutions, extracting insights from complex datasets and applying machine learning algorithms to solve real-world problems."
]
        """,
    },
    {
        "input": """
A result-oriented developer who obtained good knowledge and experience in Java
programming, including additional skills such as resolving product or service issues,
determining the cause and diagnosing non-obvious problems, and finding solutions
for solving them. I am familiar with Java Core and frameworks and popular testing
technologies. My main goal is profesional growth and gaining new skills.""",
        "correct_sentences": """
[
    None,
    None,
    "My main goal is professional growth and gaining new skills."
]""",
    },
    
]


def get_prompt_template():
    example_prompt = PromptTemplate(input_variables=["input", "correct_sentences"], template=template)
    return FewShotPromptTemplate(
        examples=examples, 
        example_prompt=example_prompt, 
        suffix="Input text: {input}", 
        input_variables=["input"],
    )