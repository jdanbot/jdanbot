from .parse_arguments import parse_arguments
from ..config import _


def get_text(func):
    @parse_arguments(1, without_params=True)
    async def wrapper(message, query=None):
        reply = message.reply_to_message

        if query:
            text = query
        elif reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        else:
            await message.reply(_("errors.few_args", num=1), parse_mode="Markdown")
            return

        return await func(message, text)

    return wrapper
