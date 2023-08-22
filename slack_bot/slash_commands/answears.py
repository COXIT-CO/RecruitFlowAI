"""Processing answears for slack slash commands"""
import json
from enum import Enum
from slack_bot.settings import env_settings


class Commands(Enum):
    GEN_JOB_DESC = "generate_job_description"
    CREATE_MEDIA_POST = "create_social_media_post"
    MATCH_RESUMES = "match_resumes"
    SCAN_RESUME = "scan_resume"
    GET_CHATS = "get_chats"


def get_answear(command: str):
    with open(env_settings.bot_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if command == Commands.GEN_JOB_DESC.value:
            return f"""<{data['generate_job_description']["url"]}|*Create Job Description*>
*Hint:* {data['generate_job_description']["desc"]}"""
        elif command == Commands.CREATE_MEDIA_POST.value:
            return f"""<{data['create_social_media_post']["url"]}|*Create Social Media Post*>
*Hint:* {data['create_social_media_post']["desc"]}"""
        elif command == Commands.MATCH_RESUMES.value:
            return f"""<{data['match_resumes']["url"]}|*Resume Matching*>
*Hint:* {data['match_resumes']["desc"]}"""
        elif command == Commands.SCAN_RESUME.value:
            return f"""<{data['scan_resume']["url"]}|*Resume Scan for Mistakes*>
*Hint:* {data['scan_resume']["desc"]}"""
        elif command == Commands.GET_CHATS.value:
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
