import json
import subprocess
import traceback
from pprint import pformat

from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.utils.markdown import code

from ..config import bot, router
from ..database import Member
from ..filters import IsSuperuser, GetText
from shellous import sh


@router.message(
    Command("e", "pe"), IsSuperuser(), GetText(disable_reply=True)
)
async def supereval(
    message: types.Message, command: CommandObject, query: str
):
    q = [f"\n {line}" for line in query.split("\n")]
    q[-1] = q[-1].replace("\n ", "\n return ")

    exec("async def __ex(message, reply, bot, member): " + "".join(q))

    try:
        member = await Member.get_by(message)
    except Exception:
        member = None

    try:
        output = await locals()["__ex"](
            message, message.reply_to_message, bot, member
        )
    except Exception:
        output = traceback.format_exc()

    if output == "disable_stdout":
        return

    if command.command == "pe":
        output: types.Message

        return await message.reply(
            code(pformat(json.loads(output.model_dump_json())))
        )

    await message.reply(code(output))


@router.message(
    Command("jbash"), IsSuperuser(), GetText(disable_reply=True)
)
async def bash(message: types.Message, query: str):
    try:
        res = await sh(query)

    except Exception:
        res = traceback.format_exc()

    await message.reply(code(res), parse_mode="MarkdownV2")
