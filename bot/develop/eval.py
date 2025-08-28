import json
import traceback
from pprint import pformat
from types import FunctionType

from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.utils.markdown import code
from shellous import sh

from ..config import bot, router
from ..database import Member
from ..filters import GetText, IsSuperuser


@router.message(
    Command("e", "pe"), IsSuperuser(), GetText(disable_reply=True)
)
async def supereval(
    message: types.Message, command: CommandObject, query: str
):
    q = [f"\n {line}" for line in query.split("\n")]
    q[-1] = q[-1].replace("\n ", "\n return ")

    f_code = compile(
        f"async def gfg(message, reply, bot, member): {"   ".join(q)}",
        "<int>",
        "exec",
    )
    f_func = FunctionType(f_code.co_consts[0], globals(), "gfg")

    try:
        member = await Member.get_by(message)
    except Exception:
        member = None

    try:
        output = await f_func(
            message, message.reply_to_message, bot, member
        )
    except Exception:
        output = traceback.format_exc()

    if output == "disable_stdout":
        return

    if command.command == "pe":
        output: types.Message

        return await message.reply(
            code(pformat(json.loads(output.model_dump_json()))[:4096])
        )

    await message.reply(code(str(output)[:4096]))


@router.message(
    Command("jbash"), IsSuperuser(), GetText(disable_reply=True)
)
async def bash(message: types.Message, query: str):
    try:
        res = await sh(query)

    except Exception:
        res = traceback.format_exc()

    await message.reply(code(res), parse_mode="MarkdownV2")
