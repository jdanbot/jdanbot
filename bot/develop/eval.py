import json
import subprocess
import traceback
from pprint import pformat

from aiogram import types
from aiogram.utils.markdown import code

from .. import handlers
from ..config import bot, router
from aiogram.filters import Command
from ..filters import IsSuperuserFilter
from ..database import Member
from ..lib.models import CustomField


@router.message(Command("e", "pe"), IsSuperuserFilter())
@handlers.parse_arguments_new
async def supereval(message: types.Message, query: CustomField(str)):
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

    if message.get_command(pure=True) == "pe":
        output: types.Message

        return await message.reply(
            code(pformat(json.loads(output.as_json()))),
            parse_mode="MarkdownV2",
        )

    await message.reply(code(output), parse_mode="MarkdownV2")


@router.message(Command("jbash"), IsSuperuserFilter())
@handlers.parse_arguments_new
async def bash(message: types.Message, query: CustomField(str)):
    try:
        command = query.split()
        output = subprocess.check_output(command).decode("utf-8")

    except Exception:
        output = traceback.format_exc()

    await message.reply(code(str(output)), parse_mode="MarkdownV2")
