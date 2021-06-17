import asyncio
import re

from math import sqrt

from ..lib import handlers
from ..lib.text import bold, code
from ..config import dp, _


async def calc(query):
    return eval(query, {"__builtins__": {}})


@dp.message_handler(commands=["calc"])
async def eban(message, locale):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        await message.reply(_("errors.enter_value"))
        return

    query = options[1]

    query = query.format(
        pi=3.14
    )

    match = re.search(r"[a-zA-Zа-яА-Я]", query)
    match_symbols = re.search(r"[\[\]\^\{\}]|\*\*", query)

    if type(match).__name__ == "Match":
        await message.reply(_("errors.only_vars"))
        return

    if type(match_symbols).__name__ == "Match" and \
       message.from_user.id != 795449748:
        await message.reply(_("errors.only_vars"))
        return

    try:
        result = await asyncio.wait_for(calc(query), 1)
    except Exception as e:
        result = bold(_("errors.error")) + "\n" + code(e)

    await message.reply(str(result)[:4096], parse_mode="HTML")


@dp.message_handler(commands=["sqrt"])
@handlers.parse_arguments(2)
async def sqrt_(message, params):
    command, num = params

    try:
        res = sqrt(int(num))
    except ValueError as e:
        await message.reply(bold(_("errors.error")) + "\n" + code(e),
                            parse_mode="HTML")
        return

    await message.reply(code(res), parse_mode="HTML")
