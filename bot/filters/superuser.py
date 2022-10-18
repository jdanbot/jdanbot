from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from ..config import settings


@dataclass
class IsSuperuserFilter(BoundFilter):
    key = "is_superuser"
    is_superuser: bool | list[int]

    async def check(self, message: types.Message) -> bool:
        if isinstance(self.is_superuser, list):
            owners = settings.bot_owners + self.is_superuser
        else:
            owners = settings.bot_owners

        return message.from_user.id in owners
