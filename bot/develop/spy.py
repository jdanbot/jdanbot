from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import text

from ..config import Locale, router
from ..database import Command as dbCommand
from ..database import Member, User
from ..filters import IsSuperuser


@router.message(Command("me", "pidorme"))
async def me_info(
    message: types.Message,
    member: Member,
    _: Locale,
):
    assert message.from_user is not None, "???"

    await message.reply(
        _.templates.about_user(
            name=text(message.from_user.full_name),
            id=str(message.from_user.id),
            status_emoji=await member.get_status_emoji(),
            chats=await member.has_chats(),
            pidor_local=await member.get_pidor_count_here(),
            pidor_all=await member.get_pidor_count_anywhere(),
            usage=await member.features_used(),
        ),
        parse_mode="Markdown",
    )


@router.message(Command("stats"), IsSuperuser())
async def calc_stats(message: types.Message, _: Locale):
    member = await Member.get_by(message)

    await message.reply(
        _.templates.stats(
            chat_users=await member.get_members_count(),
            chat_commands=await member.get_chat_commands_count(),
            users=await User.count(),
            commands=await dbCommand.count(),
        ),
        parse_mode="Markdown",
    )
