import time

from .config import bot, dp
from .locale import locale
from .lib import handlers


@dp.message_handler(commands=["mute"])
@handlers.only_admins
@handlers.parse_arguments(3, True)
async def admin_mut(message, params):
    ban_time = int(params[1]) * 60
    reply = message.reply_to_message
    await bot.restrict_chat_member(message.chat.id, reply.from_user.id,
                                   until_date=time.time() + ban_time)

    ban_log = locale.ban_template.format(
        name=reply.from_user.full_name,
        banchik=message.from_user.full_name,
        userid=reply.from_user.id,
        why=params[-1] if len(params) == 3 else "не указана",
        time=params[1]
    )

    await message.reply(ban_log, parse_mode="HTML")

    if message.chat.id == -1001176998310:
        await bot.forward_message(-1001334412934,
                                  -1001176998310,
                                  reply.message_id)

        await bot.send_message(-1001334412934, ban_log,
                               parse_mode="HTML")
