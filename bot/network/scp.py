from aiogram import types

from ..lib.models import Article
from ..lib.scp import SCP

from ..config import dp, _
from .. import handlers


@dp.message_handler(commands="scp")
@handlers.get_text
@handlers.send_article
async def get_scp(message: types.Message, query: str) -> Article:
    scp = SCP()

    results = await scp.search(query)
    return await scp.page(results[0].url)
