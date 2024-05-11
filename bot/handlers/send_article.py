from functools import wraps

from aiogram import types

from ..config import bot
from ..lib.models import Article


def send_article(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        result: Article = await func(message, *args, **kwargs)

        if result is None:
            return

        params = result.params or {}

        if isinstance(message, types.CallbackQuery):
            message = message.message
            message.reply = message.edit_text
        elif isinstance(message, types.ChosenInlineResult):
            message.reply = bot.edit_message_text
            params |= {"inline_message_id": message.inline_message_id}

        text = result.get_text()

        params = dict(
            disable_web_page_preview=False
            if result.disable_web_page_preview
            else result.image is None,
            reply_markup=result.keyboard,
            **params,
        )
        try:
            await message.reply(
                text, parse_mode=result.parse_mode, **params
            )
        except Exception as e:
            await message.reply(text, parse_mode=None, **params)

            raise e

    return wrapper
