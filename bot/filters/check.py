from typing import override

from aiogram import types
from aiogram.filters import BaseFilter

from ..database import Chat


class Check(BaseFilter):
    keys: tuple[bool]

    def __init__(self, *keys: bool):
        for key in keys:
            if isinstance(key, str):
                raise AttributeError

        self.keys = keys

    @override
    async def __call__(
        self, message: types.Message
    ) -> bool:
        settings = await Chat.get_settings(message.chat.id)

        return all(
            getattr(settings, key.__name__)
            for key in self.keys
        )
