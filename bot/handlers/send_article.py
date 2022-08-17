from aiogram import types

from ..config import bot

from ..lib.models import Article

from functools import wraps

from aiogram.utils.markdown import hide_link
from bs4 import BeautifulSoup


def add_link_to_first_bold(text: str, link: str, title: str = None) -> str:
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
        return add_link_to_first_bold(f"<b>{title}</b>\n\n" + str(soup), link)

    return text


def send_article(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args):
        result: Article = await func(message, *args)

        if isinstance(message, types.CallbackQuery):
            message = message.message
            message.reply = message.edit_text

        if isinstance(message, types.ChosenInlineResult):
            message.reply = bot.edit_message_text

        params = result.params or {}

        text = add_link_to_first_bold(result.text, result.href, result.title)

        if result.image:
            text = hide_link(result.image) + text

        await message.reply(
            text,
            parse_mode=result.parse_mode,
            disable_web_page_preview=result.image,
            reply_markup=result.keyboard,
            **params
        )

    return wrapper
