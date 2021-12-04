from bot.lib.bash import BashOrg

from ..config import dp, _
from ..lib import handlers


@dp.message_handler(commands=["bashorg", "bashim", "b"])
@handlers.parse_arguments(2, without_params=True)
async def bashorg(message, params):
    bash = BashOrg()

    if len(params) == 1:
        quotes = await bash.random()
        quote = quotes[0]
    else:
        try:
            id = int(params[1])
        except ValueError:
            message.reply(_("errors.invalid_post_id"))
            return

        quote = await bash.quote(id)

    await message.reply(
        "<a href='https://bash.im/quote/{}'>#{}</a>, {}\n\n{}".format(
            quote.id, quote.id, quote.time, quote.text
        ),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
