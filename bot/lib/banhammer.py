import datetime
import math

from ..config import bot, dp, TIMEZONE
from ..locale import locale
from .text import prettyword


async def ban(
        blocker_message,
        blockable_message,
        time = 1,
        reason = "Причина не указана"
        ):
      
    try:
        ban_time = max(1, math.ceil(float(time)))

    except ValueError:
        bt = datetime.time.fromisoformat(time)
        ban_time = bt.hour * 60 + bt.minute

    until_date = datetime.datetime.now(TIMEZONE) + datetime.timedelta(minutes=ban_time)
    await bot.restrict_chat_member(blocker_message.chat.id, blockable_message.from_user.id,
                                   until_date=until_date.timestamp())

    time_localed=prettyword(ban_time, locale.minutes)
    unban_time=until_date.isoformat()
    
    ban_log = locale.ban_template.format(
        name=blockable_message.from_user.full_name,
        banchik=blocker_message.from_user.full_name,
        userid=blockable_message.from_user.id,
        why=reason,
        time=time,
        time_localed=time_localed,
        unban_time=unban_time
    )


    if blocker_message.chat.id == -1001176998310:
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



def __calc_ban_time(time):
    if time == 0:
        return "никогда))"

    ts = datetime.now(TIMEZONE).timestamp() + time * 60
    return TIMEZONE.localize(datetime.fromtimestamp(ts))
