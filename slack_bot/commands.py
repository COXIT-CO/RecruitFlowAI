import json
import logging
from pydantic import BaseModel, FilePath
from slack_bot.utils import is_chatcraft_url

logger = logging.getLogger(__name__)

class ChatCraftReply(BaseModel):
    title: str
    url: str
    hint: str

    def get_markdwn(self) -> str:
        return f"""<{self.url}|*{self.title}*>\n*Hint:* {self.hint}"""


class CmdReplyModel(BaseModel):
    """ Slack slash commands reply model"""
    config_file: FilePath
    generate_job_description: ChatCraftReply
    create_social_media_post: ChatCraftReply
    match_resumes: ChatCraftReply
    scan_resume: ChatCraftReply


    def __init__(self, config_file: FilePath):
        try:
            with open(config_file, "r") as f:
                super().__init__(config_file=config_file, **json.load(f))
        except OSError as e:
            logger.critical("Error loading chatcraft config file: %s", e)
            raise e

    def get_replies(self):
        for field in self:
            if isinstance(field[1], ChatCraftReply):
                yield field[1].get_markdwn()

    def get_config(self)-> str:
        with open(self.config_file, "r") as f:
            return f.read()

    def save_config(self):
        with open(self.config_file, "w") as file:
            file.write(self.model_dump_json(indent=4, exclude=["config_file"]))

    def get_response_text(self, command_name: str, command_text: str) -> str:
        """Format the data for chatcraft reply and update the model"""
        command_reply_model = getattr(self, command_name)
        if not command_text:
            return command_reply_model.get_markdwn()
        else:
            if is_chatcraft_url(command_text):
                field_name = "url"
                old_value = command_reply_model.url
                command_reply_model.url = command_reply_model.text
            elif "hint" in command_text[:10].lower():
                field_name = "hint"
                old_value = command_reply_model.hint
                command_reply_model.hint = command_text.lstrip("*Hhint: ")
            else:
                return "I can't edit this command with provided data. "\
                    "Please provide chatcraft url or the text starting with `Hint:` keyword"
            self.save_config()
            return  f"{command_name} reply changed the {field_name} from {old_value} to {command_text}"
