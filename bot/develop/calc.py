import asyncio
import re
from math import sqrt
from typing import Any

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code
from fluentogram import TranslatorRunner

from ..config import router, settings
from ..filters import GetText


async def calc(query: str) -> Any:
    return eval(query, {"__builtins__": {}})


@router.message(Command("calc"), GetText(disable_reply=True))
async def eban(
    message: types.Message, query: str, _: TranslatorRunner
):
    query = query.format(pi=3.14)

    match = re.search(r"[a-zA-Zа-яА-Я]", query)
    match_symbols = re.search(r"[\[\]\^\{\}]|\*\*", query)

    if type(match).__name__ == "Match":
        await message.reply(_.errors.only_vars())
        return

    if (
        type(match_symbols).__name__ == "Match"
        and message.from_user.id not in settings.bot_owners
    ):
        await message.reply(_.errors.only_vars())
        return

    result = await asyncio.wait_for(calc(query), 1)

    await message.reply(code(result)[:4096])


@router.message(Command("sqrt"), GetText(disable_reply=True))
async def sqrt_(message, query: str):
    await message.reply(code(sqrt(query)))
