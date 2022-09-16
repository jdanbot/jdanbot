from dataclasses import dataclass
from typing import Any

from aiogram import types

from .chat import ChatMock
from .user import UserMock
from .lib import append_to_replies


@dataclass
class MessageMock:
    text: str

    message_id: int = 0
    reply_to_message: "MessageMock" = None
    chat: ChatMock = ChatMock()

    from_user: UserMock = UserMock()

    parse_mode: str = None
    disable_web_page_preview: bool = False
    reply_markup: types.InlineKeyboardMarkup = None

    _is_forward: bool = False

    def __post_init__(self):
        self.replies: list[MessageMock] = []

    is_command = types.Message.is_command
    get_full_command = types.Message.get_full_command
    get_command = types.Message.get_command
    get_args = types.Message.get_args

    @append_to_replies
    async def reply(self, text: Any, **kwargs) -> "MessageMock":
        return MessageMock(text.strip() if isinstance(text, str) else text, **kwargs)

    @property
    def replies_text(self) -> tuple[str]:
        return tuple(map(lambda x: x.text, self.replies))

    answer = reply
    reply_photo = reply
    edit_text = reply

    async def answer_chat_action(self, *args, **kwargs) -> None:
        pass

    def is_forward(self) -> bool:
        return self._is_forward
