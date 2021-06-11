import time
from datetime import datetime

from .config import bot, dp, TIMEZONE, polls, conn
from .lib import handlers
from .lib.text import prettyword
from .lib.banhammer import ban, warn, unwarn


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


@dp.message_handler(commands=["unwarn"])
@handlers.only_admins
@handlers.parse_arguments(2, True)
async def admin_unwarn(message, params):
    reply = message.reply_to_message
    await unwarn(message, reply)


@dp.message_handler(commands=["katz_poll", "poll"])
@handlers.parse_arguments(2)
async def kz_poll(message, params):
    options = ["Да", "Нет", "Воздержусь"]

    if message.chat.id == -1001334412934:
        options.append("Нет прав")

    poll = await bot.send_poll(message.chat.id, params[1],
                               options, is_anonymous=False)

    if poll.chat.id == -1001334412934:
        await poll.pin(disable_notification=True)
        await polls.add_poll(chat_id=message.chat.id,
                             user_id=message.from_user.id,
                             poll_id=poll.message_id,
                             description=params[1])
        await conn.commit()

    await message.delete()
