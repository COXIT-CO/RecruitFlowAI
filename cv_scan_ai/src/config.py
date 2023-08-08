import os
from dotenv import load_dotenv

load_dotenv('../.env')

openai_api_key = os.getenv('OPENAI_API_KEY')
openai_model = os.getenv('OPENAI_MODEL', "gpt-3.5-turbo")
