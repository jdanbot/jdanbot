from aiogram import types
from random import choice

from ..config import router
from ..database import Note, str2bool
from aiogram.filters import (
    IS_MEMBER,
    IS_NOT_MEMBER,
    ChatMemberUpdatedFilter,
)
from .legacy import triggers


@router.chat_member(
    ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER)
)
async def left_john(message: types.Message):
    chat_id = message.chat.id

    welcome = await Note.get(
        chat_id, "__enable_greatings__", False, str2bool
    )
    welcome = welcome or await Note.get(
        chat_id, "__enable_welcome__", False, str2bool
    )

    if welcome and message.from_user.id == 795449748:
        trigger = choice(triggers["jdan_welcome"])

    elif welcome:
        trigger = choice(triggers["welcome"])

    else:
        trigger = None

    if trigger:
        await message.reply(f"{trigger} ушел?")
