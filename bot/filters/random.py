from dataclasses import dataclass

from random import randint

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class WithRandomFilter(BoundFilter):
    key = "with_random"
    with_random: bool

    async def check(self, message: types.Message) -> bool:
        return randint(0, 1) == 0  # nosec
