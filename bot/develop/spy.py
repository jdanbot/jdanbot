from aiogram import types
from aiogram.utils.markdown import code, escape_md

from ..config import _, bot, dp, settings
from ..database import Command, Member


@dp.message_handler(commands=["me", "pidorme"])
async def me_info(message: types.Message):
    member = await Member.get_by(message)

    user = await bot.get_chat_member(
        message.chat.id, message.from_user.id
    )

    await message.reply(
        _(
            "spy.about_user",
            name=escape_md(message.from_user.full_name),
            id=message.from_user.id,
            chats=code(await member.get_in_chats_count()),
            status=code(user.status),
            pidor_all=await member.user.get_pidor_count(),
            pidor_local=await member.get_pidor_count(),
        ),
        parse_mode="MarkdownV2",
    )


@dp.message_handler(
    lambda message: message.from_user.id in settings.bot_owners,
    commands=["stats"],
)
async def calc_stats(message: types.Message):
    member = await Member.get_by(message)

    print(member.chat.id)

    await message.reply(
        _(
            "spy.users_info",
            chat_users=await member.chat.get_members_count(),
            chat_commands=await member.chat.get_commands_count(),
            users=await User.count(),
            commands=await Command.count(),
        ),
        parse_mode="MarkdownV2",
    )
