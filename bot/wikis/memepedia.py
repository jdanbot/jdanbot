from aiogram import types

from fluentogram import TranslatorRunner
import pymemeru

from aiogram.filters import Command
from ..config import router
from .. import handlers
from ..lib.models import Article
from ..filters import GetText

from tghtml import TgHTML


@router.message(
    Command("memepedia", "meme"), GetText(disable_reply=True)
)
@handlers.send_article
async def mempep(
    message: types.Message, query: str, _: TranslatorRunner
) -> Article:
    try:
        search = await pymemeru.search(query)
    except AttributeError:
        await message.reply(_.not_found())
        return

    page = await pymemeru.page(search[0].name)
    text = TgHTML(str(page.cleared_text), ["img"]).parsed

    return Article(
        text=text,
        image=page.main_image,
        href=f"https://memepedia.ru/{search[0].name}",
        title=page.title,
        force_format=True,
    )
