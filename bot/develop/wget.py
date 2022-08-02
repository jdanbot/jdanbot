import json

import yaml
from aiogram import types

from .lib.convert_bytes import convert_bytes
from ..config import dp, _
from .. import handlers
from ..lib.aioget import aioget
from ..lib.text import code


@dp.message_handler(commands=["d"])
@handlers.only_jdan
@handlers.get_text
async def download(message: types.Message, query: str):
    response = await aioget(query)
    text = response.text

    try:
        text = yaml.dump(json.loads(text))
    except json.decoder.JSONDecodeError:
        pass

    await message.reply(code(text[:4096]),
                        parse_mode="HTML")


@dp.message_handler(commands=["wget", "r", "request"])
@handlers.only_jdan
@handlers.parse_arguments(1)
async def wget(message: types.Message, url: str):
    response = await aioget(url)

    await message.reply(_(
        "dev.wget",
        url=url,
        code=response.status_code,
        code_emoji=["🟡", "🟢", "🟡", "🔴", "🔴"][
            int(str(response.status_code)[0]) - 1
        ],
        size=convert_bytes(len(response.content)),
        time=str(response.elapsed)
    ), parse_mode="Markdown")
