from typing import Optional

from aiogram import F, types
from aiogram.filters import Command, CommandObject
from wikipya.clients import MediaWiki
from wikipya.constants import WGR_FLAG, WRW_FLAG
from wikipya.models import Page


from httpx import URL

from ..config import router
from ..filters import GetText
from ..lib.models import Article
from .send_article import send_article

from .tghtml import TgHTML


async def more_cool_wiki_search(
    wiki: MediaWiki, query: str | int
) -> tuple[Page, str | int, str]:
    if isinstance(query, str):
        return await wiki.get_all(query)

    page_name = await wiki.get_page_name(query)

    opensearch = await wiki.opensearch(page_name)
    result = opensearch.results[0]

    page = await wiki.page(page_name)

    try:
        image = await wiki.image(page.title)
        image = WRW_FLAG if image.source == WGR_FLAG else image.source

    except Exception:
        image = None

    return page, image or -1, result.link


def wikipya_handler(
    *prefix, extract_query_from_url=False, went_trigger_command=False
):
    def argument_wrapper(func):
        @router.message(Command(*prefix), GetText(disable_reply=True))
        @router.callback_query(F.data.startswith(prefix[0] + " "))
        @send_article
        async def wrapper(
            message: types.Message, query: str, command: CommandObject
        ) -> Article:
            if extract_query_from_url:
                url = URL(query)
                query = url.path.split("/")[-1].replace("_", " ")

            answer = (
                (message, message.text)
                if went_trigger_command
                else (message,)
            )

            if "command" in func.__annotations__.keys():
                kw = {"command": command}
            else:
                kw = {}

            wiki: MediaWiki = (
                await func(*answer, **kw)
            ).get_instance()

            if query.startswith("id_"):
                query = int(query.removeprefix("id"))

            page, image, url = await more_cool_wiki_search(
                wiki, query
            )

            page_text = page.text
            is_fandom = "fandom.com" in url

            if is_fandom:
                page2 = await wiki.page(page.title, section=1)
                page3 = await wiki.page(page.title, section=2)

                page_text = (
                    page_text
                    + page2.text[: page2.text.find("<h3>")]
                    + page3.text[: page3.text.find("<h3>")]
                )

            x = TgHTML(
                page_text,
                blocklist=[
                    "div.navigation-not-searchable",
                    "table",
                    ".error",
                    ".noprint",
                    ".thumb",
                    "span.error",
                    "span.mw-ext-cite-error",
                    "p.hatnote",
                    "div#toc",
                ],
            )

            image: Optional[str] = (
                None if image in (-1, "-1") else image
            )

            return Article(
                text=x.output or "",
                href=url,
                image=image,
                title=page.title,
                disable_web_page_preview=not bool(image),
            )

        return wrapper

    return argument_wrapper
