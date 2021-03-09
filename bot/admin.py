import time

from .lib import handlers
from .config import bot, dp


@dp.message_handler(commands=["mute"])
@handlers.only_admins
@handlers.parse_arguments(3, True)
async def admin_mut(message, params):
    ban_time = int(params[1]) * 60
    reply = message.reply_to_message
    await bot.restrict_chat_member(message.chat.id, reply.from_user.id,
                                   until_date=time.time() + ban_time)

    ban_template = "Выдан мут на имя <b>{name}</b>\n\n" + \
                   "<b>Причина:</b> {why}\n" + \
                   "<b>Срок:</b> <code>{time}</code> минут"

    await message.reply(ban_template.format(
        name=reply.from_user.full_name,
        why=params[-1] if len(params) == 3 else "не указана",
        time=params[1]
    ), parse_mode="HTML")
