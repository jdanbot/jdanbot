from random import choice

from aiogram import types
from aiogram.filters import (
    IS_MEMBER,
    IS_NOT_MEMBER,
    ChatMemberUpdatedFilter,
)

from ..config import router
from ..database import Member, Note, str2bool
from .legacy import triggers


@router.chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def on_john_join(message: types.Message):
    chat_id = message.chat.id

    if await Note.get(chat_id, "__polish_mode__", False, str2bool):
        await Member.get_by_message(message)
        await message.delete()
        return

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
        await message.reply(f"{trigger}?")

    rules = await Note.get(message.chat.id, "__rules__")

    if rules is None:
        return

    try:
        await message.answer(rules)
    except Exception:
        await message.answer(rules, parse_mode=None)
