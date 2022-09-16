from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from ..config import bot
from ..lib.admin import check_admin


@dataclass
class IsAdminFilter(BoundFilter):
    key = "is_admin"
    is_admin: bool

    async def check(self, message: types.Message) -> bool:
        return message.chat.type == "supergroup" and await check_admin(
            bot, message.chat.id, message.from_user.id
        )
