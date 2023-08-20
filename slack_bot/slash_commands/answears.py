import json
from enum import Enum
from slack_bot.settings import env_settings


class Commands(Enum):
    gen_job_desc = "generate_job_description"
    create_media_post = "create_social_media_post"
    match_resumes = "match_resumes"
    scan_resume = "scan_resume"
    get_chats = "get_chats"


def get_answear(command: str):
    with open(env_settings.bot_data_path, 'r') as f:
        data = json.load(f)
        if command == Commands.gen_job_desc.value:
            return f"""<{data['generate_job_description']["url"]}|*Create Job Description*>
*Hint:* {data['generate_job_description']["desc"]}"""
        elif command == Commands.create_media_post.value:
            return f"""<{data['create_social_media_post']["url"]}|*Create Social Media Post*>
*Hint:* {data['create_social_media_post']["desc"]}"""
        elif command == Commands.match_resumes.value:
            return f"""<{data['match_resumes']["url"]}|*Resume Matching*>
*Hint:* {data['match_resumes']["desc"]}"""
        elif command == Commands.scan_resume.value:
            return f"""<{data['scan_resume']["url"]}|*Resume Scan for Mistakes*>
*Hint:* {data['scan_resume']["desc"]}"""
        elif command == Commands.get_chats.value:
            return f"""Hi! Here is the list of chats that you can use:
1. <{data['generate_job_description']["url"]}|*Create Job Description*>
*Hint:* {data['generate_job_description']["desc"]}
2. <{data['create_social_media_post']["url"]}|*Create Social Media Post*>
*Hint:* {data['create_social_media_post']["desc"]}
3. <{data['match_resumes']["url"]}|*Resume Matching*>
*Hint:* {data['match_resumes']["desc"]}
4. <{data['scan_resume']["url"]}|*Resume Scan for Mistakes*>
*Hint:* {data['scan_resume']["desc"]}
"""
        else:
            return f"Unknown command: {command}"