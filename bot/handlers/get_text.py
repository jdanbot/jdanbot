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
        elif reply and reply.photo:
            with io.BytesIO() as file:
                await reply.photo[-1].download(destination_file=file)
                file.seek(0)

                #TODO: Add custom languages

                text = pytesseract.image_to_string(Image.open(file))
                await message.reply(text)
        else:
            try:
                await message.reply(
                    _(f"docs.{func.__name__}"),
                    parse_mode="Markdown"
                )
            except AttributeError:
                await message.reply(
                    _("errors.few_args", num=1),
                    parse_mode="Markdown"
                )

            return

        return await func(message, text)

    return wrapper
