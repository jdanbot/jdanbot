import contextlib
import json

import humanize
import yaml
from aiogram import types

from .. import handlers
from ..config import _, dp
from ..lib.aioget import aioget
from ..lib.models import CustomField
from ..lib.text import code


@dp.message_handler(commands=["d"], is_superuser=True)
@handlers.get_text
async def download(message: types.Message, query: str):
    response = await aioget(query)
    text = response.text

    with contextlib.suppress(json.decoder.JSONDecodeError):
        text = yaml.dump(json.loads(text))

    await message.reply(code(text[:4096]),
                        parse_mode="HTML")


@dp.message_handler(commands=["wget", "r", "request"], is_superuser=True)
@handlers.parse_arguments_new
async def wget(message: types.Message, url: CustomField(str)):
    response = await aioget(url)

    await message.reply(_(
        "dev.wget",
        url=url,
        code=response.status_code,
        code_emoji=["🟡", "🟢", "🟡", "🔴", "🔴"][
            int(str(response.status_code)[0]) - 1
        ],
        size=humanize.naturalsize(len(response.content), binary=True),
        time=str(response.elapsed)
    ), parse_mode="Markdown")
