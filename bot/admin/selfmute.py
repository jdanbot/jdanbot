from datetime import timedelta

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)

from ..config import Locale, router
from ..database import ChatSettings
from ..filters import Arguments, Check
from .mute import BanHammer

escape_md = md.quote
bold = md.bold


@router.message(
    Command("selfmute", "selfban"),
    Check(
        ChatSettings.enable_admin,
        ChatSettings.enable_selfmute,
    ),
    Arguments(),
)
async def selfmute(
    message: types.Message, args: BanHammer, _: Locale
):
    if args.until > timedelta(weeks=1):
        await message.reply(
            bold(_.ban.selfmute_limit_reached)
        )
        return

    user = message.from_user
    assert user

    await message.reply(
        _.ban.selfmute(
            admin=user.mention_markdown(),
            why=escape_md(args.reason),
            time=escape_md(args.human_delta),
            unban_time=escape_md(args.human_until),
        )
    )

    await message.chat.restrict(
        user.id,
        until_date=args.until_date,
        permissions=types.ChatPermissions(),
    )

    await message.delete()
