from random import randint

from aiogram import types
from aiogram.filters import BaseFilter


class WithRandom(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return randint(0, 1) == 0
