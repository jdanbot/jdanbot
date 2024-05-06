from dataclasses import dataclass

from random import randint

from aiogram import types
from aiogram.filters import BaseFilter


@dataclass
class WithRandomFilter(BaseFilter):
    key = "with_random"
    with_random: bool

    async def __call__(self, message: types.Message) -> bool:
        return randint(0, 1) == 0  # nosec
