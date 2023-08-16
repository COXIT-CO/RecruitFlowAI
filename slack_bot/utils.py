import json
from pydantic import BaseModel
from enum import Enum

class ChatLink(BaseModel):
    url: str
    desc: str

class CommandResponses(BaseModel):
    generate_job_description: ChatLink
    create_social_media_post: ChatLink
    match_resumes: ChatLink
    scan_resume: ChatLink

class Commands(Enum):
    gen_job_desc = "generate_job_description"
    create_media_post = "create_social_media_post"
    match_resumes = "match_resumes"
    scan_resume = "scan_resume"
    get_chats = "get_chats"

def format_single_chat(chat: ChatLink):
    return f"""*Use this* <{chat.url}|*chat template*>\n*Instructions:* {chat.desc}"""

def format_allchats(chats: CommandResponses):
    return f"""Hi! Here is the list of chats that you can use:
1. <{chats.generate_job_description.url}|*Create Job Description*>
*Instructions:* {chats.generate_job_description.desc}
2. <{chats.create_social_media_post.url}|*Create Social Media Post*>
*Instructions:* {chats.create_social_media_post.desc}
3. <{chats.match_resumes.url}|*Resume Matching*>
*Instructions:* {chats.match_resumes.desc}
4. <{chats.scan_resume.url}|*Resume Scan for Mistakes*>
*Instructions:* {chats.scan_resume.desc}
"""

def fetch_data(command: str):
    with open('data/links.json', 'r') as f:
        data = json.load(f)
        if command != Commands.get_chats.value:
            return ChatLink(**data[command])
        else:
            return CommandResponses(**data)


def get_answear(command: str):
    data = fetch_data(command)
    if command == Commands.get_chats.value:
        return format_allchats(data)
    else:
        return format_single_chat(data)