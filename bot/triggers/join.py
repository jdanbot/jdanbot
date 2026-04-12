from random import choice

from aiogram import types
from aiogram.filters import (
    IS_MEMBER,
    IS_NOT_MEMBER,
    ChatMemberUpdatedFilter,
)

from ..config import router
from ..database import ChatSettings, Member
from .legacy import triggers


@router.chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
)
async def on_john_join(
    message: types.Message,
    member: Member,
    settings: ChatSettings,
):
    if settings.enable_kick_on_join:
        await Member.get_by(message)
        await message.delete()
        return

    if (
        message.from_user
        and message.from_user.id == 795449748
    ):
        trigger = choice(triggers["jdan_welcome"])
    elif settings.enable_welcome:
        trigger = choice(triggers["welcome"])
    else:
        trigger = None

    if trigger:
        await message.reply(f"{trigger}?")

    if (rules := member.chat.rules) is None:
        return

    try:
        await message.answer(rules)
    except Exception:
        await message.answer(rules, parse_mode=None)
