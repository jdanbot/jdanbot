from aiogram import types
from aiogram.filters import Command

from .. import handlers
from ..config import router
from ..filters import GetText
from ..lib.models import Article
from .lib.scp import SCP


@router.message(Command("scp"), GetText())
@handlers.send_article
async def scp(message: types.Message, query: str) -> Article:
    scp = SCP()

    return await scp.page(f"scp-{query.removeprefix('scp-')}")
