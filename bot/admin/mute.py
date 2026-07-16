from typing import Self

import humanize
import pytimeparse2 as pytimeparse
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)
from msgspec import Struct
from whenever import (
    Instant,
    TimeDelta,
    ZonedDateTime,
    hours,
)

from bot.config import bot

from ..config import Locale, router
from ..database.chat import ChatSettings
from ..filters import Arguments, Check, IsAdmin

escape_md = md.quote


class BanHammer(Struct, frozen=True):
    until: TimeDelta
    until_date: ZonedDateTime
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
        time = max(30, min(31622400, int(time)))

        delta = TimeDelta(seconds=time)
        date = Instant.now() + delta

        return BanHammer(
            until=delta,
            until_date=date.to_tz("UTC"),
            reason=reason,
            human_delta=BanHammer.get_human_delta(
                time, _.lang
            ),
            human_until=BanHammer.get_human_date(
                date.to_tz("Europe/Moscow")
            ),
        )

    @staticmethod
    def get_human_delta(
        seconds: int,
        lang: str,
    ) -> str:
        humanize.i18n.activate(
            None if lang == "en" else lang
        )

        return humanize.precisedelta(seconds)

    @staticmethod
    def get_human_date(date: ZonedDateTime) -> str:
        is_today = (
            date - ZonedDateTime.now("UTC")
        ) < hours(20)

        return date.format(
            "DD.MM.YYYY hh:mm" if not is_today else "hh:mm"
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
        until_date=args.until_date.timestamp(),
        permissions=types.ChatPermissions(),
    )

    if settings.admin_chat:
        await reply.forward(settings.admin_chat)
        await bot.send_message(settings.admin_chat, log)

    await message.delete()
