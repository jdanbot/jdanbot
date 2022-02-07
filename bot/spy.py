from aiogram import types
from peewee import fn, SQL

from bot.database import chat_member

from .config import bot, dp, _
from .database import Command, ChatMember, Chat, User
from .lib.text import code, prettyword, fixHTML


def _user_counter(users: int) -> str:
    return prettyword(users, _("cases.users"))


def _command_counter(users: int) -> str:
    return prettyword(users, _("cases.commands"))


@dp.message_handler(commands=["me"])
async def me_info(message: types.Message):
    member = ChatMember.get_by_message(message)
    chats = (
        ChatMember.select(fn.Count(SQL("*")))
                  .join(Chat, on=ChatMember.chat_id == Chat.id)
                  .join(User, on=ChatMember.user_id == User.id)
                  .where(ChatMember.user.id == message.from_user.id)
    ).count()

    user = await bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    await message.reply(_(
        "spy.about_user",
        name=fixHTML(message.from_user.full_name),
        id=code(message.from_user.id),
        chats=code(chats),
        status=code(user.status)
    ), parse_mode="HTML")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["stats"])
async def calc_stats(message: types.Message):
    chat_users = (
        ChatMember.select()
                  .join(Chat, on=ChatMember.chat_id == Chat.id)
                  .where(Chat.id == message.chat.id)
    ).count()

    chats_users = (
        ChatMember.select(fn.Count(SQL("*")))
    ).count()

    chat_commands = (
        Command.select(fn.Count(SQL("*")))
               .join(ChatMember, on=ChatMember.id == Command.member_id)
               .join(Chat, on=Chat.id == ChatMember.chat_id)
               .where(Chat.id == message.chat.id)
    ).count()

    chats_commands = (
        Command.select(fn.Count(SQL("*")))
    ).count()

    # TODO: REWRITE: Пиздецовый стиль сообщения

    await message.reply(code(_(
        "spy.users_info",
        local_users=chat_users,
        lu_label=_user_counter(chat_users),

        local_commands=chat_commands,
        lc_label=_command_counter(chat_commands),


        global_users=chats_users,
        gu_label=_user_counter(chats_users),

        global_commands=chats_commands,
        gc_label=_command_counter(chats_commands)
    )), parse_mode="HTML")
