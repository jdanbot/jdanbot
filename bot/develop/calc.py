import asyncio
import re
from math import sqrt
from typing import Any

from aiogram import types

from .. import handlers
from ..config import _, dp, settings
from ..lib.models import CustomField
from ..lib.text import code


async def calc(query: str) -> Any:
    return eval(query, {"__builtins__": {}})


@dp.message_handler(commands=["calc"])
@handlers.parse_arguments_new
async def eban(message: types.Message, query: CustomField(str)):
    query = query.format(pi=3.14)

    match = re.search(r"[a-zA-Zа-яА-Я]", query)
    match_symbols = re.search(r"[\[\]\^\{\}]|\*\*", query)

    if type(match).__name__ == "Match":
        await message.reply(_("errors.only_vars"))
        return

    if type(match_symbols).__name__ == "Match" and message.from_user.id not in settings.bot_owners:
        await message.reply(_("errors.only_vars"))
        return

    result = await asyncio.wait_for(calc(query), 1)

    await message.reply(str(result)[:4096], parse_mode="HTML")


@dp.message_handler(commands=["sqrt"])
@handlers.parse_arguments_new
async def sqrt_(message, num: CustomField(int)):
    await message.reply(code(sqrt(num)), parse_mode="HTML")
