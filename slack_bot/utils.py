import re

chatcraft_url_regex = re.compile(
    r"^https?://chatcraft\.org/c/[a-zA-Z0-9/]+/?$")

def is_chatcraft_url(url: str) -> bool:
    return chatcraft_url_regex.match(url) is not None
