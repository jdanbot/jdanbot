from typing import Optional

from aiogram import types
from datetime import datetime, timedelta

import math

from ..config import bot, TIMEZONE, Warn, _, Note
from .text import prettyword


async def ban(
    message: types.Message,
    reply: types.Message,
    time: int = 1,
    reason: Optional[str] = None,
    is_repost_allowed: bool = True
):
    if reason is None:
        reason = _("ban.reason_not_found")

    try:
        ban_time = max(1, math.ceil(float(time)))

    except ValueError:
        try:
            bt = datetime.time.fromisoformat(time)
        except ValueError:
            # TODO: Add to localization
            await message.reply("Введи валидное кол-во минут")
            return

        ban_time = bt.hour * 60 + bt.minute

    now = datetime.now(TIMEZONE)

    one_day = now + timedelta(days=1)
    until_date = now + timedelta(minutes=ban_time)

    await bot.restrict_chat_member(message.chat.id, reply.from_user.id,
                                   until_date=until_date.timestamp())

    unban_time = until_date.isoformat(sep=" ").split(".")[0]

    if one_day > until_date:
        unban_time = unban_time.split(" ")[1]

    is_selfmute = reply.from_user.id == message.from_user.id
    time_localed = prettyword(ban_time, _("cases.minutes"))

    name = {"name": reply.from_user.full_name} if not is_selfmute else {}

    ban_log = _(
        f"ban.{'mute' if not is_selfmute else 'selfmute'}",
        banchik=message.from_user.full_name,
        userid=reply.from_user.id,
        why=reason,
        time=str(ban_time),
        time_localed=time_localed,
        unban_time=unban_time,
        **name
    )

    if message.chat.id == -1001176998310 and is_repost_allowed:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  reply.message_id)

        await bot.send_message(-1001334412934, ban_log,
                               parse_mode="HTML")

    try:
        await bot.send_message(reply.chat.id, ban_log,
                               reply_to_message_id=reply.message_id,
                               parse_mode="HTML")

        if message.message_id != reply.message_id:
            await message.delete()
    except Exception:
        await message.reply(ban_log, parse_mode="HTML")


async def warn(
    message: types.Message,
    reply: types.Message,
    reason: Optional[str] = None
):
    if reason is None:
        reason = _("ban.reason_not_found")

    try:
        WARNS_TO_BAN = int(Note.get(message.chat.id, "__warns_to_ban__"))
    except Exception:
        WARNS_TO_BAN = 3

    wtbans = await Warn.count_warns(reply.from_user.id,
                                    reply.chat.id,
                                    period=timedelta(hours=23))
    wtbans += 1

    warn_log = _(
        "ban.warn",
        name=reply.from_user.full_name,
        banchik=message.from_user.full_name,
        userid=reply.from_user.id,
        why=reason,
        i=wtbans
    )

    if reply.chat.id == -1001176998310:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  reply.message_id)
        await bot.send_message(-1001334412934, warn_log,
                               parse_mode="HTML")

    await reply.reply(warn_log, parse_mode="HTML")

    Warn.mark_chat_member(reply.from_user.id,
                          reply.chat.id,
                          message.from_user.id,
                          reason=reason)

    if wtbans >= WARNS_TO_BAN:
        await ban(message, reply, "1440",
                  _("ban.warn_limit_reached", i=wtbans))
    else:
        await message.delete()


async def unwarn(message: types.Message, reply: types.Message):
    user_id = reply.from_user.id

    if user_id == message.from_user.id:
        await message.reply(_("ban.admin_cant_unwarn_self"))
        return

    period = timedelta(hours=24)
    period_bound = int((datetime.now(TIMEZONE) - period).timestamp())

    user_warns = list(Warn.select()
                          .where(Warn.timestamp >= period_bound,
                                 Warn.user_id == user_id)
                          .order_by(-Warn.timestamp))

    if len(user_warns) == 0:
        await message.reply(_("ban.warns_not_found"))
        return

    last_warn = user_warns[0]

    (Warn.delete()
         .where(Warn.user_id == user_id,
                Warn.timestamp == last_warn.timestamp)
         .execute())

    unwarn_log = _(
        "ban.unwarn",
        name=reply.from_user.full_name,
        banchik=message.from_user.full_name,
        userid=reply.from_user.id,
        i=len(user_warns),
        why=last_warn.reason
    )

    if reply.chat.id == -1001176998310:
        await bot.forward_message(
            -1001334412934, -1001176998310, reply.message_id)

        await bot.send_message(-1001334412934, unwarn_log,
                               parse_mode="HTML")

    await reply.reply(unwarn_log, parse_mode="HTML")
    await message.delete()
