"""Helping function to check the ouput"""
import json
from pydantic.v1 import BaseModel

def print_output(output: BaseModel):
    print(json.dumps(output, sort_keys=True, indent=3))
