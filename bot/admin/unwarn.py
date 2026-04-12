from typing import Self

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)
from msgspec import Struct

from bot.config import bot

from ..config import Locale, router
from ..database import Member
from ..database.chat import ChatSettings
from ..filters import Arguments, Check, IsAdmin

escape_md = md.quote
bold = md.bold




class UnwarnHammer(Struct, frozen=True):
    reason: str

    async def parse(
        model: Self,
        message: types.Message,
        args: str,
        _: Locale,
    ):
        return UnwarnHammer(
            reason=args.strip()
            if args.strip() != ""
            else _.ban.reason_not_found,
        )


@router.message(
    Command("unwarn"),
    IsAdmin(),
    Check(ChatSettings.enable_admin),
    Arguments(),
)
async def admin_unwarn(
    message: types.Message,
    reply: types.Message,
    member: Member,
    args: UnwarnHammer,
    settings: ChatSettings,
    _: Locale,
):
    assert reply.from_user
    assert message.from_user

    admin = member
    user = await Member.get_by(reply)

    if reply.from_user.id == message.from_user.id:
        await message.reply(_.ban.admin_cant_unwarn_self)
        return

    try:
        i = await admin.unwarn(user, args.reason)
    except IndexError:
        await message.reply(bold(_.ban.warns_not_found))
        return
    else:
        await message.reply(admin_log := _.ban.unwarn(
            user=reply.from_user.mention_markdown(),
            admin=message.from_user.mention_markdown(),
            why=escape_md(args.reason),
            i=i,
        ))

    if settings.admin_chat:
        await reply.forward(settings.admin_chat)
        await bot.send_message(
            settings.admin_chat, admin_log
        )

    await message.delete()
