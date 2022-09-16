from dataclasses import dataclass

from ..config import settings

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class IsSuperuserFilter(BoundFilter):
    key = "is_superuser"
    is_superuser: bool

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in settings.bot_owners
