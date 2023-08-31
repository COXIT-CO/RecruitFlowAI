import re

chatcraft_url_regex = re.compile(
    r"^https?://chatcraft\.org/c/[a-zA-Z0-9/]+/?$")

def is_chatcraft_url(url: str) -> bool:
    return chatcraft_url_regex.match(url) is not None

AI_PROCESSING_NOTIFICATION_MSG = "processing ..."

def convert_slack_msgs_to_openai_msgs(slack_messages: list) -> list:
    """
    Converts a list of Slack messages to a format suitable for OpenAI.

    Parameters:
    slack_messages (list): A list of dictionaries where each dictionary 
    represents a Slack message. Each dictionary must contain a 'text' key 
    representing the message content. It may also contain either a 
    'client_msg_id' key (indicating a user message) or a 'bot_id' key 
    (indicating an assistant message).

    Returns:
    list: A list of dictionaries in the OpenAI message format. Each dictionary 
    contains 'role' (either 'user' or 'assistant') and 'content' (the message 
    text) keys.
    """
    openai_messages = []
    for message in slack_messages:
        if "client_msg_id" in message:
            role = "user"
        elif "bot_id" in message:
            role = "assistant"
            if content == AI_PROCESSING_NOTIFICATION_MSG: continue
        else:
            continue
        content = message["text"]

        openai_messages.append({"role": role, "content": content})
    return openai_messages
