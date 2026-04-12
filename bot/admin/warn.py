from typing import Self

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)
from msgspec import Struct

from ..config import Locale, bot, router
from ..database import ChatSettings, Member
from ..filters import Arguments, Check, IsAdmin
from .mute import BanHammer, admin_mute

escape_md = md.quote


class WarnHammer(Struct, frozen=True):
    reason: str

    async def parse(
        model: Self,
        message: types.Message,
        args: str,
        _: Locale,
    ):
        return WarnHammer(
            reason=args.strip()
            if args.strip() != ""
            else _.ban.reason_not_found,
        )


@router.message(
    Command("warn"),
    IsAdmin(),
    Check(ChatSettings.enable_admin),
    Arguments(),
)
async def admin_warn(
    message: types.Message,
    reply: types.Message,
    args: WarnHammer,
    member: Member,
    settings: ChatSettings,
    _: Locale,
):
    admin = member
    user = await Member.get_by(reply)

    assert reply.from_user
    assert message.from_user

    warn_count = await admin.warn(user, reason=args.reason)
    await reply.reply(
        admin_log := _.ban.warn(
            user=reply.from_user.mention_markdown(),
            admin=message.from_user.mention_markdown(),
            why=md.quote(args.reason),
            i=warn_count,
        )
    )

    if settings.admin_chat:
        await reply.forward(settings.admin_chat)
        await bot.send_message(
            settings.admin_chat, admin_log
        )

    await message.delete()

    if warn_count >= settings.warns_to_ban:
        await admin_mute(
            message,
            settings,
            await BanHammer.parse(
                model=BanHammer,
                message=message,
                args=f"1d {_.ban.warn_limit_reached(i=warn_count)}",
                _=_,
            ),
            _,
        )
