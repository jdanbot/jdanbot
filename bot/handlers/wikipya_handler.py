import urllib

from aiogram import types
from wikipya.clients import MediaWiki
from wikipya.constants import WGR_FLAG, WRW_FLAG
from wikipya.models import Page

from ..config import dp
from ..lib.models import Article, CustomField
from .parse_arguments import parse_arguments_new
from .send_article import send_article


async def more_cool_wiki_search(wiki: MediaWiki, query: str | int) -> tuple[Page, str, str]:
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

    return page, image, result.link


def wikipya_handler(
    *prefix,
    extract_query_from_url=False,
    went_trigger_command=False
):
    def argument_wrapper(func):
        @dp.message_handler(commands=prefix)
        @dp.callback_query_handler(lambda x: x.data.startswith(f"{prefix[0]} "))
        @send_article
        @parse_arguments_new
        async def wrapper(
            message: types.Message,
            query: CustomField(lambda x: x)
        ) -> Article:
            if extract_query_from_url:
                url = query.split("/")
                query = url[-1]
                query = urllib.parse.unquote(query, encoding='utf-8', errors='replace').replace("_", " ")

            answer = (message, message.text) if went_trigger_command else (message,)

            wiki: MediaWiki = (await func(*answer)).get_instance()

            if query.startswith("id"):
                query = int(query.removeprefix("id"))

            page, image, url = await more_cool_wiki_search(wiki, query)

            return Article(
                page.parsed,
                href=url,
                image=image,
                disable_web_page_preview=image is None,
            )

        return wrapper
    return argument_wrapper
