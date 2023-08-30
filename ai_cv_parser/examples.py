"""Reading all examples and formatting them"""
import os
import json
from typing import Sequence, Tuple, Dict, Any

curr_dir = os.path.dirname(__file__)


def read_examples()->Sequence[Tuple[str, Dict[str, Any]]]:
    contents, expected_results = {}, {}
    dir_ = os.path.join(curr_dir, "examples")
    for path in os.listdir(dir_):
        name, extension = path.split(".")
        with open(os.path.join(dir_, path), encoding="utf-8") as f:
            if extension == "txt":
                contents[name] = f.read()
            elif extension == "json":
                expected_results[name] = json.load(f)
    return [(value, expected_results[name]) for name, value,  in contents.items()]
