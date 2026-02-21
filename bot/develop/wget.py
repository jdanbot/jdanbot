import time

import humanize
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code
from msgspec import json, toml

from ..config import Locale, router
from ..filters import GetText, IsSuperuser
from ..lib.aioget import aioget


@router.message(
    Command("d"),
    IsSuperuser(),
    GetText(disable_reply=True),
)
async def download(message: types.Message, query: str):
    r, text = await aioget(query)

    try:
        text = toml.encode(json.decode(text))
    except Exception as e:
        raise e

    await message.reply(
        code(text[:4080]),
    )


@router.message(
    Command("wget", "request", "r"),
    IsSuperuser(),
    GetText(disable_reply=True),
)
async def wget(
    message: types.Message, query: str, _: Locale
):
    start = time.perf_counter()
    res, text = await aioget(query, disable_text_loading=False)
    end = time.perf_counter() - start

    await message.reply(
        _.templates.wget(
            url=query,
            code=res.status,
            code_emoji=["🟡", "🟢", "🟡", "🔴", "🔴"][
                int(str(res.status)[0]) - 1
            ],
            size=humanize.naturalsize(
                len(text), binary=True
            ),
            time=f"{round(end, 3)}s",
        ),
        parse_mode="Markdown",
    )
