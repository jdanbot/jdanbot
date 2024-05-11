from aiogram import types
from aiogram.utils.markdown import code, text

from aiogram.filters import Command
from ..filters import IsSuperuser
from ..config import bot, router
from ..database import Command as dCommand, Member, User

from fluentogram import TranslatorRunner


@router.message(Command("me", "pidorme"))
async def me_info(message: types.Message, _: TranslatorRunner):
    member = await Member.get_by(message)

    user = await bot.get_chat_member(
        message.chat.id, message.from_user.id
    )

    await message.reply(
        _.user.info(
            name=text(message.from_user.full_name),
            id=str(message.from_user.id),
            chats=code(await member.get_in_chats_count()),
            status=code(user.status.value),
            pidor_all=await member.user.get_pidor_count(),
            pidor_local=await member.get_pidor_count(),
        ),
        parse_mode="MarkdownV2",
    )


@router.message(Command("stats"), IsSuperuser())
async def calc_stats(message: types.Message, _: TranslatorRunner):
    member = await Member.get_by(message)

    await message.reply(
        _.user.stats(
            chat_users=await member.chat.get_members_count(),
            chat_commands=await member.chat.get_commands_count(),
            users=await User.count(),
            commands=await dCommand.count(),
        ),
        parse_mode="MarkdownV2",
    )
