import pymemeru
from aiogram import types
from aiogram.filters import Command
from tghtml import TgHTML

from ..config import Locale, router
from ..filters import GetText
from ..lib.models import Article


@router.message(
    Command("memepedia", "meme"),
    GetText(disable_reply=True),
)
async def mempep(
    message: types.Message, query: str, _: Locale
) -> Article:
    try:
        search = await pymemeru.search(query)
    except AttributeError:
        await message.reply(_.errors.not_found)
        return

    page = await pymemeru.page(search[0].name)
    text = TgHTML(str(page.cleared_text)).parsed

    return Article(
        text=text,
        image=page.main_image,
        href=f"https://memepedia.ru/{search[0].name}",
        title=page.title,
        force_format=True,
    )
