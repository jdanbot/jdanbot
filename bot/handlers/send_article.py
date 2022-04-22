from aiogram import types

from ..config import bot

from aiogram.utils.markdown import hide_link
from bs4 import BeautifulSoup


def send_article(func):
    async def wrapper(message: types.Message, *args):
        result = await func(message, *args)

        if result.inline:
            action = bot.edit_message_text
            params = result.params
        else:
            action = message.reply
            params = {}

        if result.image and not result.test:
            await message.answer_chat_action("upload_photo")
            await message.reply_photo(
                result.image,
                caption=result.text,
                parse_mode=result.parse_mode,
                reply_markup=result.keyboard,
            )
        elif result.image:
            if isinstance(message, types.CallbackQuery):
                message = message.message
                message.reply = message.edit_text

            soup = BeautifulSoup(result.text, "lxml")

            b = soup.find_all("b")

            if len(b) != 0:
                if result.href is not None:
                    b = b[0]
                    b.name = "a"
                    b["href"] = result.href
                    b = b.wrap(soup.new_tag("b"))

            text = hide_link(result.image) + unbody(soup)

            await action(
                text,
                parse_mode=result.parse_mode,
                disable_web_page_preview=result.disable_web_page_preview,
                reply_markup=result.keyboard,
                **params
            )
        else:
            if isinstance(message, types.CallbackQuery):
                message = message.message
                message.reply = message.edit_text

            await message.reply(
                result.text,
                parse_mode=result.parse_mode,
                disable_web_page_preview=result.disable_web_page_preview,
                reply_markup=result.keyboard,
            )

    return wrapper



def unbody(html):
    return str(html).replace("<p>", "").replace("</p>", "") \
                    .replace("<html><body>", "") \
                    .replace("</body></html>", "")
