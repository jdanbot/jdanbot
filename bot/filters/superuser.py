from dataclasses import dataclass

from aiogram import types
from aiogram.filters import BaseFilter

from ..config import settings


@dataclass
class IsSuperuserFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in settings.bot_owners
