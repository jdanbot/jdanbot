from functools import wraps

from aiogram import types
from aiogram.utils import exceptions
from aiogram.utils.markdown import hide_link
from bs4 import BeautifulSoup

from ..config import bot
from ..lib.models import Article


def make_first_bold_a_link(text: str, link: str, title: str | None = None) -> str:
    if link is None:
        return text

    soup = BeautifulSoup(text, "html.parser")
    b = soup.find_all(["b", "strong"])

    if len(b) != 0:
        b = b[0]
        b.name = "a"
        b["href"] = link
        b = b.wrap(soup.new_tag("b"))

        return str(soup)

    if title:
        return make_first_bold_a_link(f"<b>{title}</b>\n\n{str(soup)}", link)

    return text


def send_article(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args):
        result: Article = await func(message, *args)

        if result is None:
            return

        params = result.params or {}

        if isinstance(message, types.CallbackQuery):
            message = message.message
            message.reply = message.edit_text
        elif isinstance(message, types.ChosenInlineResult):
            message.reply = bot.edit_message_text
            params |= {"inline_message_id": message.inline_message_id}

        text = ""

        if result.image:
            text += hide_link(result.image)

        if result.href:
            text += make_first_bold_a_link(result.text, result.href, result.title)
        else:
            text += result.text

        try:
            await message.reply(
                text,
                parse_mode=result.parse_mode,
                disable_web_page_preview=result.image is None
                if not result.disable_web_page_preview
                else False,
                reply_markup=result.keyboard,
                **params,
            )
        except exceptions.CantParseEntities as e:
            await message.reply(
                text,
                parse_mode=None,
                disable_web_page_preview=result.image is None
                if not result.disable_web_page_preview
                else False,
                reply_markup=result.keyboard,
                **params,
            )

            raise e

    return wrapper
