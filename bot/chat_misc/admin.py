from aiogram import types

from .lib.banhammer import BanHammer, WarnHammer, UnwarnHammer
from ..config import bot, dp, _
from ..schemas import Poll
from .. import handlers

from ..schemas import ChatMember


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
@handlers.parse_arguments(2, True)
async def self_mut(message: types.Message, *args):
    action = BanHammer(message, message, *args)

    if await action.execute():
        await action.log()
    else:
        await message.reply(_("ban.selfmute_limit_reached"))


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


@dp.message_handler(commands=["poll"])
@handlers.check("enable_poll")
@handlers.parse_arguments(1)
async def kz_poll(message: types.Message, name: str):
    options = ["Да", "Нет", "Воздержусь"]
    is_katz_bots = message.chat.id == -1001334412934

    if is_katz_bots:
        options.append("Нет прав")

    poll = await bot.send_poll(
        message.chat.id,
        name,
        options,
        is_anonymous=False
    )

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

    await message.answer_poll(
        reply.question,
        [option.text for option in reply.options],
        is_anonymous=False,
        allows_multiple_answers=reply.allows_multiple_answers
    )
