from typing import Callable

from aiogram.filters import Command

from bot.config.lib.locales import locales
from bot.database.member import Member
from bot.filters import Arguments

from .bot import BotMock
from .callback import CallbackMock
from .chat import ChatMock
from .message import MessageMock
from .user import UserMock

user_a: UserMock = UserMock(
    username="test",
    first_name="user",
    last_name="testowy",
)

chat_a = ChatMock()


async def mock(
    func: Callable[[str], None],
    command: str,
    from_user: UserMock = user_a,
    **kwargs: dict[str, str],
) -> str:
    message_mock = MessageMock(
        text=command,
        from_user=from_user,
        chat=chat_a,
    )

    anns = func.__annotations__
    kw = {}

    if "_" in anns:
        kw["_"] = locales.ru
    if "command" in anns:
        kw["command"] = Command.extract_command(
            text=command
        )
    if "query" in anns:
        _, kw["query"] = command.split(" ", 1)
    if "member" in anns:
        kw["member"] = await Member.get_by(message_mock)
    if "args" in anns:
        kw["args"] = await Arguments.parse(
            message_mock,
            anns["args"],
            command.split(" ", maxsplit=1)[1],
            locales.ru,
        )

    await func(message=message_mock, **kw, **kwargs)

    return message_mock.answer_text


__all__ = (
    BotMock,
    CallbackMock,
    ChatMock,
    MessageMock,
    UserMock,
    mock,
)
