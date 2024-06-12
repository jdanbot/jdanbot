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
        text = result.get_text()

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
            await message.reply(text, parse_mode=None, **params)

    return wrapper
