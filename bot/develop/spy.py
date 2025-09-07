from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code, text

from ..config import Locale, bot, router
from ..database import Command as dCommand
from ..database import Member, User
from ..filters import IsSuperuser


@router.message(Command("me", "pidorme"))
async def me_info(message: types.Message, _: Locale):
    member = await Member.get_by(message)
    user = await bot.get_chat_member(
        message.chat.id, message.from_user.id
    )

    await message.reply(
        _.templates.about_user(
            name=text(message.from_user.full_name),
            id=str(message.from_user.id),
            status=code(user.status.value),
            pidor_local=await member.get_pidor_events_count(),
            pidor_all=await member.get_pidor_count(),
        ),
        parse_mode="Markdown",
    )


@router.message(Command("stats"), IsSuperuser())
async def calc_stats(message: types.Message, _: Locale):
    member = await Member.get_by(message)

    await message.reply(
        _.templates.stats(
            chat_users=await member.get_members_count(),
            chat_commands=await member.chat.get_commands_count(),
            users=await User.count(),
            commands=await dCommand.count(),
        ),
        parse_mode="Markdown",
    )
