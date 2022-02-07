from aiogram import types

from .config import bot, dp, Poll, _
from .timer import youtube_task
from .lib import handlers
from .lib.banhammer import BanHammer, WarnHammer, UnwarnHammer

from .database import ChatMember


@dp.message_handler(commands=["mute"])
@handlers.check("__enable_admin__")
@handlers.only_admins
@handlers.parse_arguments(2, True)
async def admin_mut(message: types.Message, *args):
    reply = message.reply_to_message

    action = BanHammer(message, reply, *args)

    await action.execute()
    await action.log()

    if message.chat.id == -1001176998310:
        await action.repost()



@dp.message_handler(commands=["selfmute", "selfban"])
@handlers.check("__enable_admin__")
@handlers.check("__enable_selfmute__")
@handlers.parse_arguments(1, True)
async def self_mut(message: types.Message, *args):
    action = BanHammer(message, message, *args)

    await action.execute()
    await action.log()


@dp.message_handler(commands=["warn"])
@handlers.check("__enable_admin__")
@handlers.only_admins
@handlers.parse_arguments(1, True)
async def admin_warn(message: types.Message, *args):
    reply = message.reply_to_message

    action = WarnHammer(message, reply, *args)

    await action.log()
    await action.execute()

    if message.chat.id == -1001176998310:
        await action.repost()


@dp.message_handler(commands=["unwarn"])
@handlers.check("__enable_admin__")
@handlers.only_admins
@handlers.parse_arguments(1, True)
async def admin_unwarn(message: types.Message, *args):
    reply = message.reply_to_message

    if reply.from_user.id == message.from_user.id:
        await message.reply(_("ban.admin_cant_unwarn_self"))
        return

    try:
        action = UnwarnHammer(message, reply, *args)
    except IndexError:
        await message.reply(_("ban.warns_not_found"))
        return

    await action.execute()
    await action.log()

    if message.chat.id == -1001176998310:
        await action.repost()


@dp.message_handler(commands=["katz_poll", "poll"])
@handlers.parse_arguments(1)
async def kz_poll(message: types.Message, name: str):
    options = ["Да", "Нет", "Воздержусь"]
    is_katz_bots = message.chat.id == -1001334412934

    if is_katz_bots:
        options.append("Нет прав")

    poll = await bot.send_poll(message.chat.id, name,
                               options, is_anonymous=False)

    if is_katz_bots:
        await poll.pin(disable_notification=True)
        Poll.insert(
            id=poll.message_id,
            author_id=ChatMember.get_by_message(message).id,
            description=name).execute()

    await message.delete()


@dp.message_handler(commands=["open"])
async def open_poll(message: types.Message):
    reply = message.reply_to_message.poll
    await message.answer_poll(reply.question,
                              [option.text for option in reply.options],
                              is_anonymous=False)


@dp.message_handler(commands=["reload_pin"])
@handlers.only_admins
async def repin(message: types.Message):
    if message.chat.id != -1001176998310:
        return

    KATZ_CHANNEL = "UCUGfDbfRIx51kJGGHIFo8Rw"
    await youtube_task(KATZ_CHANNEL, message.chat.id)
