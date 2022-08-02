from aiogram import types

import asyncio
import re

from math import sqrt
from typing import Any

from .. import handlers
from ..lib.text import code
from ..config import dp, _


async def calc(query: str) -> Any:
    return eval(query, {"__builtins__": {}})


@dp.message_handler(commands=["calc"])
@handlers.parse_arguments(1)
async def eban(message: types.Message, query: str):
    query = query.format(pi=3.14)

    match = re.search(r"[a-zA-Zа-яА-Я]", query)
    match_symbols = re.search(r"[\[\]\^\{\}]|\*\*", query)

    if type(match).__name__ == "Match":
        await message.reply(_("errors.only_vars"))
        return

    if type(match_symbols).__name__ == "Match" and \
       message.from_user.id != 795449748:
        await message.reply(_("errors.only_vars"))
        return

    result = await asyncio.wait_for(calc(query), 1)

    await message.reply(str(result)[:4096], parse_mode="HTML")


@dp.message_handler(commands=["sqrt"])
@handlers.parse_arguments(1)
async def sqrt_(message, num):
    res = sqrt(int(num))
    await message.reply(code(res), parse_mode="HTML")
