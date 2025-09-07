from aiogram import types
from aiogram.filters import Command

from ..config import router
from ..filters import GetText
from ..lib.models import Article
from .lib.scp import SCP


@router.message(Command("scp"), GetText())
async def scp(
    message: types.Message, query: str
) -> Article:
    return await SCP.page(
        f"scp-{query.removeprefix('scp-')}"
    )
