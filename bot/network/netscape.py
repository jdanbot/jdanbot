from aiogram import types
from aiogram.filters import Command
from tghtml import TgHTML

from ..config import router
from ..filters import GetText, IsSuperuser
from ..lib.aioget import aioget
from ..lib.models import Article


@router.message(
    Command("netscape", "net"),
    IsSuperuser(),
    GetText(disable_reply=True),
)
async def netscape(
    message: types.Message, query: str
) -> Article:
    res, text = await aioget(query)

    html = TgHTML(text, enable_preprocess=True)

    return Article(
        text=str(html),
        href=query,
        parse_mode="HTML",
        force_add_title=True,
    )
