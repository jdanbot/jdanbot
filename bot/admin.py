import time
from datetime import datetime

from .config import bot, dp, TIMEZONE
from .locale import locale
from .lib import handlers
from .lib.text import prettyword
from .lib.banhammer import ban


@dp.message_handler(commands=["mute"])
@handlers.only_admins
@handlers.parse_arguments(3, True)
async def admin_mut(message, params):
    reply = message.reply_to_message
    ban(message, reply, *params[1:])
 
 
@dp.message_handler(commands=["selfmute"])
@handlers.parse_arguments(2, False)
async def self_mut(message, params):
    ban(message, message, *params[1:])


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
