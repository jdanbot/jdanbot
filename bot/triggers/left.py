from random import choice

from aiogram import types
from aiogram.filters import (
    IS_MEMBER,
    IS_NOT_MEMBER,
    ChatMemberUpdatedFilter,
)

from ..config import router
from ..database import ChatSettings
from .legacy import triggers


@router.chat_member(
    ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def left_john(
    message: types.Message,
    settings: ChatSettings,
):
    if (
        settings.enable_welcome
        and message.from_user
        and message.from_user.id == 795449748
    ):
        trigger = choice(triggers["jdan_welcome"])

    elif settings.enable_welcome:
        trigger = choice(triggers["welcome"])

    else:
        trigger = None

    if trigger:
        await message.reply(f"{trigger} ушел?")
