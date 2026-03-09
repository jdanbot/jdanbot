from dataclasses import dataclass
from ..database import Note, str2bool

from aiogram import types
from aiogram.filters import BaseFilter


@dataclass
class Check(BaseFilter):
    keys: list[str]

    def __init__(self, *keys):
        self.keys = keys

    async def __call__(self, message: types.Message) -> bool | None:
        print("Rewrite check!!!")
        return [True for key in self.keys]

        if all(
            [
                await Note.get(
                    message.chat.id, key, default=True, type=str2bool
                )
                for key in self.keys
            ]
        ):
            return True
