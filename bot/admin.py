import time
from datetime import datetime

from .config import bot, dp, TIMEZONE
from .locale import locale
from .lib import handlers
from .lib.text import prettyword


@dp.message_handler(commands=["mute"])
@handlers.only_admins
@handlers.parse_arguments(3, True)
async def admin_mut(message, params):
    reply = message.reply_to_message

    try:
        ban_time = float(params[1])
    except ValueError:
        bt = datetime.time.fromisoformat(params[1])
        ban_time = bt.hour + bt.minute

    until_date = time.time() + ban_time * 60
    await bot.restrict_chat_member(message.chat.id, reply.from_user.id,
                                   until_date=until_date)

    ban_log = locale.ban_template.format(
        name=reply.from_user.full_name,
        banchik=message.from_user.full_name,
        userid=reply.from_user.id,
        why=params[-1] if len(params) == 3 else "не указана",
        time=params[1],
        time_localed=prettyword(ban_time, locale.minutes),
        unban_time=calc_ban_time(ban_time).strftime("%Y-%m-%d %H:%M:%S")
    )

    if message.chat.id == -1001176998310:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  reply.message_id)

        await bot.send_message(-1001334412934, ban_log,
                               parse_mode="HTML")

    try:
        await message.delete()
        await bot.send_message(message.chat.id, ban_log,
                               reply_to_message_id=reply.message_id,
                               parse_mode="HTML")
    except Exception:
        await message.reply(ban_log, parse_mode="HTML")


<<<<<<< HEAD
@dp.message_handler(commands=["selfmute"])
@handlers.parse_arguments(2, True)
async def self_mut(message, params):
    try:
        ban_time = float(params[1])
    except ValueError:
        bt = datetime.time.fromisoformat(params[1])
        ban_time = bt.hour + bt.minute

    until_date = time.time() + ban_time * 60
    await bot.restrict_chat_member(message.chat.id, message.from_user.id,
                                   until_date=until_date)

    ban_log = locale.ban_template.format(
        name=message.from_user.full_name,
        banchik=message.from_user.full_name,
        userid=message.from_user.id,
        why="самобан",
        time=params[1],
        time_localed=prettyword(ban_time, locale.minutes),
        unban_time=calc_ban_time(ban_time).strftime("%Y-%m-%d %H:%M:%S")
    )

    if message.chat.id == -1001176998310:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  reply.message_id)

        await bot.send_message(-1001334412934, ban_log,
                               parse_mode="HTML")

    try:
        await message.delete()
        await bot.send_message(message.chat.id, ban_log,
                               reply_to_message_id=reply.message_id,
                               parse_mode="HTML")
    except Exception:
        await message.reply(ban_log, parse_mode="HTML")


=======
>>>>>>> origin/Aphanasiy
def calc_ban_time(time):
    if time == 0:
        return "никогда))"

    ts = datetime.now(TIMEZONE).timestamp() + time * 60
    return TIMEZONE.localize(datetime.fromtimestamp(ts))


@dp.message_handler(commands=["katz_poll"])
@handlers.parse_arguments(2)
async def kz_poll(message, params):
    await bot.send_poll(message.chat.id, params[1], [
                            "Да",
                            "Нет",
                            "Воздержусь",
                            "Нет прав"
                        ], is_anonymous=False)
    await message.delete()
