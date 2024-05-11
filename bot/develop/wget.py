import contextlib
import json

import humanize
import yaml
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code

from fluentogram import TranslatorRunner

from ..config import router
from ..filters import GetText, IsSuperuser
from ..lib.aioget import aioget


@router.message(
    Command("d"), IsSuperuser(), GetText(disable_reply=True)
)
async def download(message: types.Message, query: str):
    response = await aioget(query)
    text = response.text

    with contextlib.suppress(json.decoder.JSONDecodeError):
        text = yaml.dump(json.loads(text))

    await message.reply(
        code(text[:4096]),
    )


@router.message(
    Command("wget", "request", "r"),
    IsSuperuser(),
    GetText(disable_reply=True),
)
async def wget(
    message: types.Message, query: str, _: TranslatorRunner
):
    res = await aioget(query)

    await message.reply(
        _.wget(
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
