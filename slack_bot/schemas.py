import json
from urllib.parse import parse_qsl
from pydantic import BaseModel, FilePath
from fastapi import Depends, Request

async def with_body(request: Request) -> bytes:
    """Return request body.

    Per design, a route cannot depend on a form field and consume body because
    dependencies resolution consumes body.
    Therefore, this is not using `fastapi.Form` to extract form data parameters.
    """
    return await request.body()


def with_form_data(body: bytes = Depends(with_body)) -> dict:
    return dict(parse_qsl(body.decode()))


class Command(BaseModel):
    """Model of incoming request from slack slash commands """
    token: str
    team_id: str
    team_domain: str
    channel_id: str
    channel_name: str
    user_id: str
    user_name: str
    command: str
    response_url: str
    trigger_id: str
    api_app_id: str
    text: str = None
    enterprise_id: str = None
    enterprise_name: str = None

    def __init__(self, form_data: dict = Depends(with_form_data)):
        super().__init__(**form_data)


class ChatCraftReply(BaseModel):
    title: str
    url: str
    desc: str

    def get_markdwn(self) -> str:
        return f"""<{self.url}|*{self.title}*>\n*Hint:* {self.desc}"""


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

    @property
    def get_chats(self):
        return "Hi! Here is the list of chats that you can use:\n " + \
            "\n".join([f"{i+1}. {str(field)}" for i, field in enumerate(self.__fields__.values())])

    def save_model(self):
        """Saves model to the file everytime the data was changed"""
        with open(self.file_path, "w") as file:
            file.write(self.model_dump_json(indent=4, exclude=["file_path"]))
