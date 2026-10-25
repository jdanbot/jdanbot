from collections.abc import Awaitable
from typing import Any, Callable, override

from aiogram import BaseMiddleware, types
from aiogram.filters import Command as CommandFilter
from tghtml import TgHTML
from wikipya.clients import Fandom, MediaWiki, Wikipedia

from ...config import bot
from ...database import Command, Member
from ...lib.models import Article


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
        event: types.TelegramObject,
        data: dict[str, Any],
    ):
        if isinstance(event, types.Message):
            message = event

        is_guest_message = message.guest_query_id
        me = await bot.me()

        if is_guest_message:
            message = message.model_copy(
                update=dict(
                    text=(message.text or "")
                    .replace(f"@{me.username}", "")
                    .strip()
                )
            )
            data["command"] = None

        command_orig = CommandFilter.extract_command(
            text=message.text
        )

        command = command_orig.command
        args = command_orig.args

        member = await Member.get_by(message)

        try:
            data["reply"] = message.reply_to_message
        except Exception:
            pass

        if command is not None:
            data["member"] = member
            data["settings"] = member.chat.settings

            await Command(
                id=None,
                user_id=member.user_id,
                chat_id=member.chat_id,
                name=command.lower(),
                args=args or "",
            ).save()

        for (
            lcommand_raw
        ) in member.chat.settings.locked_commands:
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

            if isinstance(res, str):
                await message.reply_document(
                    types.BufferedInputFile(
                        res.encode("UTF-8"),
                        f"{query.removesuffix('SOURCE').strip()}.html",
                    )
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

        page, image, url = await wiki.fetch_all(
            query=query, close_session=False
        )

        page_text: str = page.text
        is_fandom = "fandom.com" in url

        if (
            is_fandom
            or len(
                parse_html(
                    page_text, wiki.tag_blocklist
                ).parsed
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
            except Exception:
                raise

        await wiki.close()

        if send_original_html:
            return page_text

        if page_text.strip().endswith("</h2>"):
            page_text = page_text[: page_text.rfind("<h2>")]

        x = parse_html(page_text, wiki.tag_blocklist)

        image: str | None = (
            None if image in (-1, "-1") else image
        )

        try:
            image = image.source
        except Exception:
            pass

        return Article(
            text=x.parsed.replace("&lt;translate&gt;", "") or "",
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
        elif message.guest_query_id and not result.image:
            await message.answer_guest_query(
                types.InlineQueryResultArticle(
                    id="1",
                    title="test",
                    input_message_content=types.InputTextMessageContent(
                        message_text=text,
                        parse_mode=result.parse_mode,
                        **params,
                    ),
                )
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
