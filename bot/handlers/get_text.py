import io
from aiogram import types
from PIL import Image
import pytesseract

from .parse_arguments import parse_arguments
from ..config import _

from functools import wraps


def get_text(func):
    @wraps(func)
    @parse_arguments(1, without_params=True)
    async def wrapper(message: types.Message, query=None):
        reply = message.reply_to_message

        if query:
            text = query
        elif reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        else:
            try:
                text = _(f"docs.{func.__name__}")

                if text.startswith("docs."):
                    raise AttributeError()

                await message.reply(text, parse_mode="markdown")
            except AttributeError:
                await message.reply(
                    _("errors.few_args", num=1),
                    parse_mode="Markdown"
                )

            return

        return await func(message, text)

    return wrapper
