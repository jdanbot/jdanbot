import datetime
import math

from ..config import bot, TIMEZONE, Warn, conn, _, Note, manager
from .text import prettyword


async def ban(
    blocker_message,
    blockable_message,
    time=1,
    reason=None,
    isRepostAllowed=True
):
    if reason is None:
        reason = _("ban.reason_not_found")

    try:
        ban_time = max(1, math.ceil(float(time)))

    except ValueError:
        try:
            bt = datetime.time.fromisoformat(time)
        except ValueError:
            await blocker_message.reply("Введи валидное кол-во минут")
            return

        ban_time = bt.hour * 60 + bt.minute

    until_date = datetime.datetime.now(TIMEZONE) + datetime.timedelta(minutes=ban_time)
    await bot.restrict_chat_member(blocker_message.chat.id, blockable_message.from_user.id,
                                   until_date=until_date.timestamp())

    time_localed=prettyword(ban_time, _("cases.minutes"))
    unban_time=until_date.isoformat()
    is_selfmute = blockable_message.from_user.id == blocker_message.from_user.id

    name = {"name": blockable_message.from_user.full_name} if not is_selfmute else {}

    ban_log = _(
        f"ban.{'mute' if not is_selfmute else 'selfmute'}",
        banchik=blocker_message.from_user.full_name,
        userid=blockable_message.from_user.id,
        why=reason,
        time=str(ban_time),
        time_localed=time_localed,
        unban_time=unban_time,
        **name
    )

    if blocker_message.chat.id == -1001176998310 and isRepostAllowed:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  blockable_message.message_id)

        await bot.send_message(-1001334412934, ban_log,
                               parse_mode="HTML")

    try:
        await bot.send_message(blockable_message.chat.id, ban_log,
                               reply_to_message_id=blockable_message.message_id,
                               parse_mode="HTML")

        if blocker_message.message_id != blockable_message.message_id:
            await blocker_message.delete()
    except Exception:
        await blocker_message.reply(ban_log, parse_mode="HTML")


async def warn(
    blocker_message,
    blockable_message,
    reason=None
):
    if reason is None:
        reason = _("ban.reason_not_found")

    try:
        WARNS_TO_BAN = int(await Note.get(
            blocker_message.chat.id, "__warns_to_ban__"))

    except Exception:
        WARNS_TO_BAN = 3

    wtbans = await Warn.count_wtbans(blockable_message.from_user.id,
                                     blockable_message.chat.id,
                                     period=datetime.timedelta(hours=23))
    wtbans += 1

    warn_log = _(
        "ban.warn",
        name=blockable_message.from_user.full_name,
        banchik=blocker_message.from_user.full_name,
        userid=blockable_message.from_user.id,
        why=reason,
        i=wtbans
    )

    if blockable_message.chat.id == -1001176998310:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  blockable_message.message_id)
        await bot.send_message(-1001334412934, warn_log,
                               parse_mode="HTML")

    await blockable_message.reply(warn_log, parse_mode="HTML")

    await Warn.mark_chat_member(blockable_message.from_user.id,
                                blockable_message.chat.id,
                                blocker_message.from_user.id,
                                reason=reason)

    if wtbans >= WARNS_TO_BAN:
        await ban(blocker_message, blockable_message, "1440",
                  _("ban.warn_limit_reached", i=wtbans))
    else:
        await blocker_message.delete()


async def unwarn(blocker_message, blockable_message):
    user_id = blockable_message.from_user.id

    if user_id == blocker_message.from_user.id:
        await blocker_message.reply(_("ban.admin_cant_unwarn_self"))
        return

    period = datetime.timedelta(hours=24)
    period_bound = int((datetime.datetime.now() - period).timestamp())

    user_warns = list(await manager.execute(
        Warn.select()
            .where(Warn.timestamp >= period_bound,
                   Warn.user_id == user_id)
            .order_by(-Warn.timestamp)
    ))

    if len(user_warns) == 0:
        await blocker_message.reply(_("ban.warns_not_found"))
        return

    last_warn = user_warns[0]

    await manager.execute(
        Warn.delete()
            .where(Warn.user_id == user_id,
                   Warn.timestamp == last_warn.timestamp)
    )

    unwarn_log = _(
        "ban.unwarn",
        name=blockable_message.from_user.full_name,
        banchik=blocker_message.from_user.full_name,
        userid=blockable_message.from_user.id,
        i=len(user_warns),
        why=last_warn.reason
    )

    if blockable_message.chat.id == -1001176998310:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  blockable_message.message_id)
        await bot.send_message(-1001334412934, unwarn_log,
                               parse_mode="HTML")

    await blockable_message.reply(unwarn_log, parse_mode="HTML")
    await blocker_message.delete()
