from dataclasses import dataclass

from aiogram import types


@dataclass
class ChatMock:
    id: int = -10020000000
    type: str = "supergroup"

    title: str = "jdan's secret test chat"
    username: str = "savekanobu"

    full_name = types.Chat.full_name
