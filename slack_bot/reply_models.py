import json
from pydantic import BaseModel, FilePath
from slack_bot.utils import is_chatcraft_url


class ChatCraftReply(BaseModel):
    title: str
    url: str
    hint: str

    def get_markdwn(self) -> str:
        return f"""<{self.url}|*{self.title}*>\n*Hint:* {self.hint}"""


class CommandReplies(BaseModel):
    """ Model of incoming request from slack slash commands """
    file_path: FilePath
    generate_job_description: ChatCraftReply
    create_social_media_post: ChatCraftReply
    match_resumes: ChatCraftReply
    scan_resume: ChatCraftReply

    def __init__(self, file_path: FilePath):
        with open(file_path, "r") as f:
            super().__init__(file_path=file_path, **json.load(f))


    def iter_chatcraft_replies(self):
        for field in self:
            if isinstance(field[1], ChatCraftReply):
                yield field[1].get_markdwn()

    def save_model(self):
        """Saves model to the file everytime the data was changed"""
        with open(self.file_path, "w") as file:
            file.write(self.model_dump_json(indent=4, exclude=["file_path"]))


    def get_response_text(self, command_name: str, command_text: str) -> str:
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
            self.save_model()
            return  f"{command_name} reply changed the {field_name} from {old_value} to {command_text}"
