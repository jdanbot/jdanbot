import time

from .lib import handlers
from .config import bot, dp


@dp.message_handler(commands=["mute"])
@handlers.only_admins
@handlers.parse_arguments(2)
async def admin_mut(message, params):
    ban_time = time.time() + (int(params[1]) * 60)
    reply = message.reply_to_message
    await bot.restrict_chat_member(message.chat.id, reply.from_user.id,
                                   until_date=ban_time)

    await message.reply("Светлая ему память)")
