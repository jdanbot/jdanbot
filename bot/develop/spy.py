from aiogram import types
from peewee import fn, SQL

from aiogram.utils.markdown import code, escape_md

from ..config import bot, dp, _, settings
from ..schemas import Command as CommandOld, ChatMember, Chat, User, Pidor
from ..database import Command, Member, User as NUser


@dp.message_handler(commands=["me", "pidorme"])
async def me_info(message: types.Message):
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

    pidor_all = sum([pidor.count for pidor in (
        Pidor.select()
             .join(ChatMember, on=Pidor.member_id == ChatMember.id)
             .join(User, on=ChatMember.user_id == User.id)
             .where(User.id == message.from_user.id)
    )])

    pidor = sum([pidor.count for pidor in (
        Pidor.select()
             .join(ChatMember, on=Pidor.member_id == ChatMember.id)
             .join(User, on=ChatMember.user_id == User.id)
             .join(Chat, on=ChatMember.chat_id == Chat.id)
             .where(User.id == message.from_user.id, Chat.id == message.chat.id)
    )])

    await message.reply(_(
        "spy.about_user",
        name=escape_md(message.from_user.full_name),
        id=message.from_user.id,
        chats=code(chats),
        status=code(user.status),
        pidor_all=pidor_all,
        pidor_local=pidor
    ), parse_mode="MarkdownV2")


@dp.message_handler(lambda message: message.from_user.id in settings.bot_owners, commands=["stats"])
async def calc_stats(message: types.Message):
    # chat_users = (
    #     ChatMember.select()
    #               .join(Chat, on=ChatMember.chat_id == Chat.id)
    #               .where(Chat.id == message.chat.id)
    # ).count()

    chat_users = await Member.find(
        Member.chat.id == message.from_user.id
    ).count()

    # chat_users = len(await Member.aggregate([
    #     {
    #         "input": "$Member",
    #         "as": "member",
    #         "cond": { 
    #             "$eq": [ "$member.chat.id", message.from_user.id ]
    #         }
    #     }
    # ]).to_list())

    chat_users = len(await Member.aggregate([
        {"$lookup": {
            "from": "User",
            "let": {"user": "$User"},
            "as": "user",
            "pipeline": [{
                "$match": {
                    "$expr": {
                        "$eq": [ "$user.id", "@jDan734" ]
                    }
                }
            }]
        }}
    ]).to_list())

    # chats_users = (
    #     ChatMember.select(fn.Count(SQL("*")))
    # ).count()

    chats_users = await NUser.count()

    # chat_commands = (
    #     CommandOld.select(fn.Count(SQL("*")))
    #            .join(ChatMember, on=ChatMember.id == Command.member_id)
    #            .join(Chat, on=Chat.id == ChatMember.chat_id)
    #            .where(Chat.id == message.chat.id)
    # ).count()

    chat_commands = await Command.find(
        Command.member.chat.tgid == message.chat.id
    ).count()

    chat_commands = await Command.find(
        {"member": {"user": {"username": "@jDan734"}}},
        # {"member.user.username": "@jDan734"}
        # Command.member.user.username == "@jDan734",
        fetch_links=True
    ).count()

    print(Command.find(
        {"member": {"user": {"username": "@jDan734"}}}
        # {"member.user.username": "@jDan734"}
        # Command.member.user.username == "@jDan734",
        # fetch_links=True
    ).get_filter_query())

    # chats_commands = (
    #     Command.select(fn.Count(SQL("*")))
    # ).count()

    chats_commands = await Command.count()

    await message.reply(_(
        "spy.users_info",
        local_users=chat_users,
        local_commands=chat_commands,

        global_users=chats_users,
        global_commands=chats_commands,
    ), parse_mode="MarkdownV2")
