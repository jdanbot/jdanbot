import json

import humanize
import toml
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code

from ..config import Locale, router
from ..filters import GetText, IsSuperuser
from ..lib.aioget import aioget


@router.message(
    Command("d"), IsSuperuser(), GetText(disable_reply=True)
)
async def download(message: types.Message, query: str):
    response = await aioget(query)
    text = response.text

    try:
        text = toml.dumps(json.loads(text))
    except:
        pass

    await message.reply(
        code(text[:4096]),
    )


@router.message(
    Command("wget", "request", "r"),
    IsSuperuser(),
    GetText(disable_reply=True),
)
async def wget(
    message: types.Message, query: str, _: Locale
):
    res = await aioget(query)

    await message.reply(
        _.templates.wget(
            url=query,
            code=res.status_code,
            code_emoji=["🟡", "🟢", "🟡", "🔴", "🔴"][
                int(str(res.status_code)[0]) - 1
            ],
            size=humanize.naturalsize(len(res.content), binary=True),
            time=str(res.elapsed),
        ),
        parse_mode="Markdown",
    )
