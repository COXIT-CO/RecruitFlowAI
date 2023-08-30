import json
from pydantic.v1 import BaseModel

def print_output(output: BaseModel):
    """Pretty print output"""
    print(json.dumps(output, sort_keys=True, indent=3))
