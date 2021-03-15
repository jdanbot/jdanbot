import pymemeru

from ..config import dp
from ..lib import handlers
from ..lib.text import cuteCrop


@dp.message_handler(commands=["memepedia", "meme"])
@handlers.parse_arguments(2)
async def mempep(message, params):
    try:
        search = await pymemeru.search(params[1])
    except AttributeError:
        await message.reply("Не удалось найти")
        return

    page = await pymemeru.page(search[0]["name"])

    if page[0] == "":
        await message.reply(cuteCrop(page[1], 4096), parse_mode="HTML")
    else:
        await message.reply_photo(page[0],
                                  caption=cuteCrop(page[1], 1000),
                                  parse_mode="HTML")
