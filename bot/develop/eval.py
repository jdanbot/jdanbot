from aiogram import types

import traceback
import subprocess

from ..config import bot, dp
from ..lib.text import code
from .. import handlers


@dp.message_handler(commands=["e"])
@handlers.only_jdan
@handlers.parse_arguments(1)
async def supereval(message: types.Message, query: str):
    q = [f"\n {line}" for line in query.split("\n")]
    q[-1] = q[-1].replace("\n ", "\n return ")

    exec(
        "async def __ex(message, bot): " +
        "".join(q)
    )

    try:
        output = await locals()["__ex"](message, bot)
    except Exception:
        output = traceback.format_exc()

    if output == "disable_stdout":
        return

    await message.reply(code(output),
                        parse_mode="HTML")


@dp.message_handler(commands=["jbash"])
@handlers.only_jdan
@handlers.parse_arguments(1)
async def bash(message: types.Message, query: str):
    try:
        command = query.split()
        output = subprocess.check_output(command).decode("utf-8")

    except Exception:
        output = traceback.format_exc()

    await message.reply(code(str(output)),
                        parse_mode="HTML")
