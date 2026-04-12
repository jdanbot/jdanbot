from typing import Self

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)
from msgspec import Struct

from bot.config import bot
from bot.database.chat import ChatSettings

from ..config import Locale, router
from ..filters import Arguments, Check, IsAdmin

escape_md = md.quote


class UnbanHammer(Struct, frozen=True):
    reason: str

    async def parse(
        model: Self,
        message: types.Message,
        args: str,
        _: Locale,
    ):
        return UnbanHammer(
            reason=args.strip()
            if args.strip() != ""
            else _.ban.reason_not_found
        )


@router.message(
    Command("unmute"),
    IsAdmin(),
    Check(ChatSettings.enable_admin),
    Arguments(),
)
async def admin_unmute(
    message: types.Message,
    args: UnbanHammer,
    _: Locale,
):
    reply = message.reply_to_message
    assert reply

    user, admin = (
        reply.from_user,
        message.from_user,
    )
    assert user
    assert admin

    await message.chat.unban(user.id, only_if_banned=True)

    await reply.reply(
        admin_log := _.ban.unmute(
            admin=admin.mention_markdown(),
            user=user.mention_markdown(),
            why=args.reason,
        )
    )

    if message.chat.id == -1001176998310:
        await reply.forward(-1001334412934)
        await bot.send_message(-1001334412934, admin_log)

    await message.delete()
