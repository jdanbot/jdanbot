from aiogram import types

from .parse_arguments import parse_arguments

from functools import wraps
from fluentogram import FluentTranslator
from aiogram.filters import CommandObject


def get_text(func):
    @wraps(func)
    @parse_arguments(1, without_params=True)
    async def wrapper(
        message: types.Message,
        _: FluentTranslator,
        command: CommandObject,
        query=None,
        *args,
        **kwargs,
    ):
        reply = message.reply_to_message

        if query:
            text = query
        elif message.quote and message.quote.is_manual:
            text = message.quote.text
        elif reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        else:
            await message.reply(
                _.few_args(num=1), parse_mode="Markdown"
            )
            try:
                text = _.docs.__get__(func.__name__)()

                if text.startswith("docs."):
                    raise AttributeError()

                await message.reply(text, parse_mode="markdown")
            except (TypeError, AttributeError):
                await message.reply(
                    _.few_args(num=1), parse_mode="Markdown"
                )

            return

        return await func(
            message, text, _=_, command=command, *args, **kwargs
        )

    return wrapper
