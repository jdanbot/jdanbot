from datetime import UTC, datetime, timedelta
from typing import Self

import humanize
import pytimeparse2 as pytimeparse
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)
from msgspec import Struct

from bot.config import bot
from bot.lib.errors import JdanbotError

from ..config import Locale, router
from ..database.chat import ChatSettings
from ..database.member import MSK
from ..filters import Arguments, Check, IsAdmin

escape_md = md.quote


class BanHammer(Struct, frozen=True):
    until: timedelta
    until_date: datetime
    reason: str
    human_until: str
    human_delta: str

    async def parse(
        model: Self,
        message: types.Message,
        args: str,
        _: Locale,
    ):
        raw_args = args.split(" ", maxsplit=1)

        time, reason = (
            pytimeparse.parse(raw_args[0]),
            _.ban.reason_not_found
            if len(raw_args) == 1
            else raw_args[1].strip(),
        )

        assert time, JdanbotError("No time!")
        time = max(30, min(31622400, int(time)))

        delta = timedelta(seconds=time)
        date = datetime.now(tz=UTC) + delta

        return BanHammer(
            until=delta,
            until_date=date,
            reason=reason,
            human_delta=BanHammer.get_human_delta(
                time, _.lang
            ),
            human_until=BanHammer.get_human_date(
                date.astimezone(MSK)
            ),
        )

    @staticmethod
    def get_human_delta(seconds: int, lang: str) -> str:
        humanize.i18n.activate(
            None if lang == "en" else lang
        )

        return humanize.precisedelta(seconds)

    @staticmethod
    def get_human_date(date: datetime) -> str:
        is_today = (
            date - datetime.now(tz=MSK)
        ) < timedelta(hours=23, minutes=59)

        return date.strftime(
            "%d.%m.%Y %H:%M" if not is_today else "%H:%M"
        )


@router.message(
    Command("mute"),
    Check(ChatSettings.enable_admin),
    IsAdmin(),
    Arguments(),
)
async def admin_mute(
    message: types.Message,
    reply: types.Message,
    settings: ChatSettings,
    args: BanHammer,
    _: Locale,
):
    assert message.reply_to_message, "Where is reply?"
    reply = message.reply_to_message

    user, admin = (
        reply.from_user,
        message.from_user,
    )
    assert user
    assert admin

    log = _.ban.mute(
        admin=admin.mention_markdown(),
        user=user.mention_markdown(),
        why=escape_md(args.reason),
        time=escape_md(args.human_delta),
        unban_time=escape_md(args.human_until),
    )

    await reply.reply(log)
    await message.chat.restrict(
        user.id,
        until_date=args.until_date,
        permissions=types.ChatPermissions(),
    )

    if settings.admin_chat:
        await reply.forward(settings.admin_chat)
        await bot.send_message(settings.admin_chat, log)

    await message.delete()
