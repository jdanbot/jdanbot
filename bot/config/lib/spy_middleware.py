from collections.abc import Awaitable
from typing import Any, Callable, override

import httpx
from aiogram import BaseMiddleware, types
from aiogram.filters import Command as CommandFilter
from bs4 import BeautifulSoup as bs4
from wikipya.clients import Fandom, MediaWiki, Wikipedia

from bot.database.command import Command

from ...config import bot
from ...config.lib.tghtml import TgHTML
from ...database import Command, Member
from ...lib.models import Article


async def fetch_all(
    client: Wikipedia,
    query: str | int,
    to_section: int = 0,
    fetch_image_from_page: bool = False,
):
    if isinstance(query, int):
        query = await client.get_page_name(query)

    async with httpx.AsyncClient(
        headers={
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Accept-Encoding": "gzip",
        }
    ) as web:
        r = await web.get(
            f"{client.url}?&action=query&titles={query}&format=json"
        )

    result = None

    res = r.json()
    id_ = list(res["query"]["pages"].keys())[0]

    if id != -1:
        title = res["query"]["pages"][id_]["title"]
        page = await client.page(title, to_section=to_section)
    else:
        search = await client.search(query)
        result = search[0]

        page = await client.page(
            result.title, to_section=to_section
        )

        title = result.title

    BASE_URL = client.url.url.removesuffix(
        "/api.php"
    ).removesuffix("/w")

    try:
        opensearch = await client.opensearch(title)
        link = opensearch.results[0].link
    except:
        link = f"{BASE_URL}/wiki/{title}"

    if fetch_image_from_page:
        try:
            image = bs4(
                page.text, features="lxml"
            ).find_all("img")[0]["srcset"]
            image = BASE_URL + image.split(" ")[-2]
        except:
            image = None
    else:
        try:
            image = await client.image(page.title)
        except:
            image = None

    return page, image, link


def parse_html(source: str, blocklist: tuple) -> TgHTML:
    return TgHTML(
        source,
        blocklist=[
            "div.navigation-not-searchable",
            "table",
            ".error",
            ".noprint",
            ".thumb",
            "span.error",
            "span.mw-ext-cite-error",
            ".hatnote",
            "div#toc",
            "div.mbox-text-div",
            "span.hide-when-compact",
            "span.mbox-date",
            ".ts-disambig",
            ".ve-hide",
            ".mw-editsection",
            *blocklist,
        ],
    )


class SpyMiddleware(BaseMiddleware):
    @override
    async def __call__(
        self,
        handler: Callable[
            [types.TelegramObject, dict[str, Any]],
            Awaitable[Any],
        ],
        message: types.Message,
        data: dict[str, Any],
    ):
        command_orig = CommandFilter.extract_command(
            self=CommandFilter, text=message.text
        )

        command = command_orig.command
        args = command_orig.args

        member = await Member.get_by(message)

        locked_commands = (
            await Member.get_note("locked_commands") or ""
        ).split(" ")

        if command is not None:
            member = await Member.get_by(message)
            data["member"] = member

            await Command.create(
                user_id=member.user_id,
                chat_id=member.chat_id,
                name=command.lower(),
                args=args or "",
            )

        for lcommand_raw in locked_commands:
            lcommand = lcommand_raw.removeprefix("-")
            is_force_admin = command != lcommand_raw

            if command != lcommand:
                continue

            if (not is_force_admin) or (
                is_force_admin
                and not await member.check_admin()
            ):
                return

        res = await handler(message, data)
        mw_types = Wikipedia | Fandom | MediaWiki

        if isinstance(res, dict | tuple):
            res, query = res
        elif isinstance(res, Article):
            pass
        else:
            arguments: list[str] = message.text.split(
                " ", maxsplit=1
            )

            if len(arguments) == 2:
                query: str = arguments[1]
            else:
                return

        res_client: MediaWiki = res

        if isinstance(res, mw_types):
            res = await self.run_mediawiki_handler(
                wiki=res_client, query=query
            )

        if isinstance(res, Article):
            await self.send_article(message, res)

    async def run_mediawiki_handler(
        self, wiki: Fandom, query: int | str
    ) -> Article:
        if isinstance(query, str) and query.endswith(
            "SOURCE"
        ):
            query = query.removesuffix("SOURCE")
            send_original_html = True
        else:
            send_original_html = False

        page, image, url = await fetch_all(
            client=wiki,
            query=query,
            fetch_image_from_page=(
                "encyclopatia.ru" in wiki.url.url
            ),
        )

        page_text: str = page.text
        is_fandom = "fandom.com" in url

        if (
            is_fandom
            or len(
                parse_html(
                    page_text, wiki.tag_blocklist
                ).output
            )
            < 200
        ):
            try:
                page2 = await wiki.page(
                    page.title, section=1, to_section=2
                )

                page_text = (
                    page_text
                    + page2.text[: page2.text.find("<h3>")]
                    # + page3.text[: page3.text.find("<h3>")]
                )
            except:
                pass

        if page_text.strip().endswith("</h2>"):
            page_text = page_text[: page_text.rfind("<h2>")]

        if send_original_html:
            print(page_text)
            with open("test.html", "w") as f:
                f.write(page_text)
            return Article(
                text=page_text or "",
                href=url,
                title=page.title,
                disable_web_page_preview=True,
                parse_mode=None,
            )

        x = parse_html(page_text, wiki.tag_blocklist)

        image: str | None = (
            None if image in (-1, "-1") else image
        )

        try:
            image = image.source
        except:
            pass

        return Article(
            text=x.output or "",
            href=url,
            image=image,
            title=page.title,
            disable_web_page_preview=not bool(image),
        )

    @staticmethod
    async def send_article(
        message: types.Message, article: Article
    ) -> None:
        result = article

        params = result.params or {}
        text = result.get_text()

        if len(text) > 4096:
            text = text[:4094] + "…"

        params = dict(
            disable_web_page_preview=(
                result.disable_web_page_preview
                or result.image is None
            ),
            reply_markup=result.keyboard,
            **params,
        )

        if isinstance(message, types.CallbackQuery):
            await message.message.edit_text(
                text, parse_mode=result.parse_mode, **params
            )
            return
        elif isinstance(message, types.ChosenInlineResult):
            await bot.edit_message_text(
                text,
                parse_mode=result.parse_mode,
                inline_message_id=message.inline_message_id,
                **params,
            )
            return
        try:
            await message.reply(
                text, parse_mode=result.parse_mode, **params
            )
        except Exception:
            await message.reply(
                text, parse_mode=None, **params
            )
