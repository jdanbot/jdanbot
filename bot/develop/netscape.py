from aiogram import types
from aiogram.filters import Command
from readability import Document

from ..config import router
from ..config.lib.tghtml import TgHTML
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
    res = await aioget(query)
    html = res.text

    parsed_html = TgHTML(html, enable_preprocess=True)
    title = Document(html).title()

    return Article(
        text=str(parsed_html),
        title=title,
        href=query,
        parse_mode="HTML",
        force_add_title=True,
    )
