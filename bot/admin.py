import time
from datetime import datetime

from .config import bot, dp, TIMEZONE
from .locale import locale
from .lib import handlers
from .lib.text import prettyword
from .lib.banhammer import ban, warn


@dp.message_handler(commands=["mute"])
@handlers.only_admins
@handlers.parse_arguments(3, True)
async def admin_mut(message, params):
    reply = message.reply_to_message
    await ban(message, reply, *params[1:])


@dp.message_handler(commands=["selfmute", "selfban"])
@handlers.parse_arguments(3, True)
async def self_mut(message, params):
    await ban(message, message, *params[1:], isRepostAllowed=False)


@dp.message_handler(commands=["warn"])
@handlers.only_admins
@handlers.parse_arguments(2, True)
async def admin_warn(message, params):
    reply = message.reply_to_message
    await warn(message, reply, *params[1:])


@dp.message_handler(commands=["katz_poll"])
@handlers.parse_arguments(2)
async def kz_poll(message, params):
    poll = await bot.send_poll(message.chat.id, params[1], [
                            "Да",
                            "Нет",
                            "Воздержусь",
                            "Нет прав"
                        ], is_anonymous=False)

    if poll.chat.id == -1001334412934:
        await poll.pin(disable_notification=True)

    await message.delete()

