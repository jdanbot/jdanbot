from dataclasses import dataclass


def append_to_replies(func):    
    async def wrapper(self, *args, **kwargs):
        msg = await func(self, *args, **kwargs)
        self.replies.append(msg)

        return msg

    return wrapper


@dataclass
class MessageMock:
    text: str
    reply_to_message: "MessageMock" = None

    def __post_init__(self):
        self.replies: list[MessageMock] = []

    def is_command(self) -> str:
        text = self.text or self.caption
        return text and text.startswith("/")

    def get_full_command(self) -> str:
        if self.is_command():
            text = self.text or self.caption
            command, *args = text.split(maxsplit=1)
            args = args[0] if args else ""
            return command, args

    @append_to_replies
    async def reply(
        self,
        text: str,
        parse_mode: str = None
    ) -> "MessageMock":
        return MessageMock(
            text=text
        )
