import contextlib
from dataclasses import dataclass

from aiogram import types
from aiogram.filters import BaseFilter


from ..config import bot
from ..lib.admin import check_admin


@dataclass
class IsAdminFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        with contextlib.suppress(Exception):
            message = message.message

        return (
            message.chat.type == "supergroup"
            and await check_admin(
                bot, message.chat.id, message.from_user.id
            )
        )
