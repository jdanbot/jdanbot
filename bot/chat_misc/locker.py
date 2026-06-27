from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code

from ..config import Locale, router
from ..database import Member
from ..filters import GetText, IsAdmin


def unite(*args) -> str:
    return " ".join([*args])


@router.message(Command("locklist", "locked"), IsAdmin())
async def show_locked_(
    message: types.Message, member: Member, _: Locale
):
    locked_commands = member.chat.settings.locked_commands
    await message.reply(code(locked_commands))


@router.message(Command("lock"), GetText(), IsAdmin())
async def lock_command_(
    message: types.Message,
    member: Member,
    query: str,
    _: Locale,
):
    commands = member.chat.settings.locked_commands

    print(query)
    # TODO: add custom append & pop method
    await member.chat.set_list_setting(
        "locked_commands", set(commands) | {*query.split()}
    )

    await message.reply("l")


@router.message(Command("unlock"), GetText(), IsAdmin())
async def unlock_command_(
    message: types.Message,
    member: Member,
    query: str,
    _: Locale,
):
    locked_commands = member.chat.settings.locked_commands

    await member.chat.set_list_setting(
        "locked_commands",
        set(locked_commands) - {*query.split()},
    )
    await message.reply("u")
