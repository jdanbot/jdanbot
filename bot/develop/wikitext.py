from aiogram.filters import Command

from ..config import router
from ..filters import GetText
from wikitexthtml import Page
from pyquery import PyQuery as jq


class WikiPage(Page):
    def page_load(self, page: str) -> str:
        return page


def unwrap(i: int, tag: jq):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with(contents + "\n\n")


def rename(i: int, tag: jq, tag_name: str):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with((f"<{tag_name}>{contents}</{tag_name}>"))


@router.message(Command("wikitext"), GetText(disable_reply=True))
async def parse_wikitext(message, query: str):
    html = WikiPage(query).render().html

    try:
        await message.reply(html, parse_mode="html")
    except Exception:
        await message.reply(html, parse_mode=None)


@router.message(Command("html"), GetText(disable_reply=True))
async def parse_wikitext(message, query: str):
    html = jq(query)

    html.find("div").each(unwrap)
    html.find("ancap").each(lambda i, x: rename(i, x, "blockquote"))

    await message.reply(html.html(), parse_mode="HTML")
