from dataclasses import dataclass

from aiogram import types

from .bot import BotMock


@dataclass
class UserMock:
    id: int = 0

    username: str = None

    first_name: str = None
    last_name: str = None

    bot: BotMock = BotMock()

    full_name = types.User.full_name
    get_mention = types.User.get_mention
    url = types.User.url
