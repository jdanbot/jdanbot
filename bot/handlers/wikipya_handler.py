import urllib

from aiogram import F, types
from aiogram.filters import Command, CommandObject
from wikipya.clients import MediaWiki
from wikipya.constants import WGR_FLAG, WRW_FLAG
from wikipya.models import Page

from ..config import router
from ..filters import GetText
from ..lib.models import Article
from .send_article import send_article

from markdownify import markdownify as html2md
from markdown import markdown as md2html
from pyquery import PyQuery as jq


def unwrap(i: int, tag: jq, space: str = "\n\n", strip=False):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with(contents + space)


def remove(i: int, tag: jq):
    jq(tag).replace_with("")


def rename(i: int, tag: jq, tag_name: str):
    contents = jq(tag).html()
    if contents is None:
        jq(tag).remove()
    else:
        jq(tag).replace_with((f"<{tag_name}>{contents}</{tag_name}>"))


async def more_cool_wiki_search(
    wiki: MediaWiki, query: str | int
) -> tuple[Page, str, str]:
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
                url = query.split("/")
                query = url[-1]
                query = urllib.parse.unquote(
                    query, encoding="utf-8", errors="replace"
                ).replace("_", " ")

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

            if query.startswith("id"):
                query = int(query.removeprefix("id"))

            page, image, url = await more_cool_wiki_search(
                wiki, query
            )

            t = jq(page.text)
            t.find("table").each(remove)

            t.find("span").filter(
                lambda i, x: jq(x).attr("style")
                == "font-style:italic;"
            ).each(lambda i, x: rename(i, x, "i"))

            t.find("img").each(remove)
            t.find("sup.noexcerpt").each(remove)
            t.find("sup.reference a").each(remove)
            t.find("div.hatnote").each(remove)
            t.find("small").each(remove)
            t.find("sup.reference a").each(remove)
            t.find("a").each(lambda i, x: unwrap(i, x, ""))
            t.find("blockquote blockquote").each(
                lambda i, x: unwrap(i, x, "")
            )
            t.find("ol.references").each(remove)

            md = html2md(t.html())

            print([md])

            # clean result html
            html = md2html(md)
            tag = jq(html)

            tag.find("div").each(lambda i, x: unwrap(i, x, ""))
            tag.find("p").each(unwrap)

            print(tag)
            print(tag.html())

            return Article(
                text=str(tag.html())
                .replace("\n\n", "\n")
                .replace("<blockquote>\n", "<blockquote>"),
                href=url,
                image=image,
                disable_web_page_preview=image is None,
            )

            page.tag_blocklist += [
                "div.navigation-not-searchable",
                "table",
                ".error",
                ".noprint",
                ".thumb",
                "span.error",
                "span.mw-ext-cite-error",
                "p.hatnote",
            ]

            return Article(
                text=page.parsed,
                href=url,
                image=image,
                disable_web_page_preview=image is None,
            )

        return wrapper

    return argument_wrapper
