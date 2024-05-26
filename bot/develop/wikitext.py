from aiogram.filters import Command

from ..config import router
from ..filters import GetText
from wikitexthtml import Page


class WikiPage(Page):
    def page_load(self, page: str) -> str:
        return page


@router.message(Command("wikitext"), GetText(disable_reply=True))
async def parse_wikitext(message, query: str):
    html = WikiPage(query).render().html

    try:
        await message.reply(html, parse_mode="html")
    except Exception:
        await message.reply(html, parse_mode=None)
