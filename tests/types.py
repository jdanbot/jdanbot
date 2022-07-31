from dataclasses import dataclass
from aiogram import types


@dataclass
class BotMock:
    token: str = None

    parse_mode: str = None


@dataclass
class ChatMock:
    id: int = -10020000000

    type: str = "supergroup"
    
    title: str = "jdan's secret test chat"
    username: str = "savekanobu"

    async def restrict(self, *args, **kwargs) -> bool:
        #TODO: Implement restrict

        return True


@dataclass
class UserMock:
    id: int = 12345678

    username: str = None

    first_name: str = None
    last_name: str = None

    bot: BotMock = BotMock()

    full_name = types.User.full_name
    get_mention = types.User.get_mention
    url = types.User.url


def append_to_replies(func):    
    async def wrapper(self, *args, **kwargs):
        msg = await func(self, *args, **kwargs)
        self.replies.append(msg)

        return msg

    return wrapper


@dataclass
class MessageMock:
    text: str

    message_id: int = 0
    reply_to_message: "MessageMock" = None
    chat: ChatMock = ChatMock()

    from_user: UserMock = UserMock()

    def __post_init__(self):
        self.replies: list[MessageMock] = []

    is_command = types.Message.is_command
    get_full_command = types.Message.get_full_command
    get_command = types.Message.get_command

    @append_to_replies
    async def reply(
        self,
        text: str,
        parse_mode: str = None,
        disable_web_page_preview: bool = False
    ) -> "MessageMock":
        return MessageMock(
            text=text
        )

    answer = reply
    reply_photo = reply


    async def answer_chat_action(self, *args, **kwargs) -> None: ...


user_a = UserMock(
    username="test",

    first_name="user",
    last_name="testowy",
)

user_b = UserMock(
    id=1234,

    username="niebaneny",
    first_name="niebaneny człowiek"
)
