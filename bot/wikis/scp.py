from aiogram import types

from .lib.scp import SCP
from ..lib.models import Article

from ..config import dp, _
from .. import handlers


@dp.message_handler(commands="scp")
@handlers.get_text
@handlers.send_article
async def get_scp(message: types.Message, query: str) -> Article:
    scp = SCP()

    return await scp.page(f"scp-{query.removeprefix('scp-')}")
