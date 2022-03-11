from aiogram import types

from ..config import dp, _
from .. import handlers
from ..lib.bash import BashOrg


@dp.message_handler(commands=["bashorg", "bashim", "b"])
@handlers.parse_arguments(1, without_params=True)
async def bashorg(message: types.Message, query: int = None):
    bash = BashOrg()

    if query:
        try:
            id = int(query)
        except ValueError:
            message.reply(_("errors.invalid_post_id"))
            return

        quote = await bash.quote(id)
    else:
        quotes = await bash.random()
        quote = quotes[0]

    await message.reply(
        "<a href='https://bash.im/quote/{}'>#{}</a>, {}\n\n{}".format(
            quote.id, quote.id, quote.time, quote.text
        ),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
