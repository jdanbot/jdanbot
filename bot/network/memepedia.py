from aiogram import types

import pymemeru

from ..config import dp, _
from ..lib import handlers
from ..lib.models import Article


@dp.message_handler(commands=["memepedia", "meme"])
@handlers.send_article
@handlers.parse_arguments(1)
async def mempep(message: types.Message, query: str) -> Article:
    try:
        search = await pymemeru.search(query)
    except AttributeError:
        await message.reply(_("errors.not_found"))
        return

    page = await pymemeru.page(search[0]["name"])

    return Article(
        text=page[1],
        image=page[0]
    )
