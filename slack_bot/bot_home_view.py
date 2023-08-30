from slack_bot.commands import CmdReplyModel


def devider_block():
    return {"type": "divider"}


def mrkdwn_block(text: str):
    return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
    }

def header_block(text: str):
    return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": text
        }
    }


def get_home_blocks(cmd_replies: CmdReplyModel):
    """Provides the links of the blocks for the app home section"""
    return  [
        header_block("Follow the link below to process the candidate:"),
        devider_block(),
        *[mrkdwn_block(text) for text in cmd_replies.get_replies()],
        devider_block(),
        header_block("Current configuration file:"),
        mrkdwn_block(f"```{cmd_replies.get_config()}```")
    ]
