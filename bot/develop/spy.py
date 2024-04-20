from aiogram import types
from peewee import fn, SQL

from aiogram.utils.markdown import code, escape_md

from ..config import bot, dp, _, settings
from ..database import Command, Member, User

from pprint import pprint


@dp.message_handler(commands=["me", "pidorme"])
async def me_info(message: types.Message):
    chats = (
        ChatMember.select(fn.Count(SQL("*")))
        .join(Chat, on=ChatMember.chat_id == Chat.id)
        .join(User, on=ChatMember.user_id == User.id)
        .where(ChatMember.user.id == message.from_user.id)
    ).count()

    user = await bot.get_chat_member(message.chat.id, message.from_user.id)

    pidor_all = sum(
        [
            pidor.count
            for pidor in (
                Pidor.select()
                .join(ChatMember, on=Pidor.member_id == ChatMember.id)
                .join(User, on=ChatMember.user_id == User.id)
                .where(User.id == message.from_user.id)
            )
        ]
    )

    pidor = sum(
        [
            pidor.count
            for pidor in (
                Pidor.select()
                .join(ChatMember, on=Pidor.member_id == ChatMember.id)
                .join(User, on=ChatMember.user_id == User.id)
                .join(Chat, on=ChatMember.chat_id == Chat.id)
                .where(User.id == message.from_user.id, Chat.id == message.chat.id)
            )
        ]
    )

    await message.reply(
        _(
            "spy.about_user",
            name=escape_md(message.from_user.full_name),
            id=message.from_user.id,
            chats=code(chats),
            status=code(user.status),
            pidor_all=pidor_all,
            pidor_local=pidor,
        ),
        parse_mode="MarkdownV2",
    )


@dp.message_handler(
    lambda message: message.from_user.id in settings.bot_owners, commands=["stats"]
)
async def calc_stats(message: types.Message):
    await message.reply(
        _(
            "spy.users_info",
            local_users=await Member.find(Member.chat.tgid == message.chat.id).count(),
            local_commands=await Command.find(
                Command.chat_id == message.chat.id
            ).count(),
            global_users=await User.find_all().count(),
            global_commands=await Command.find_all().count(),
        ),
        parse_mode="MarkdownV2",
    )
