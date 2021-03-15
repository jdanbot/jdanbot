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

    try:
        page = await pymemeru.page(search[0]["name"])
    except IndexError:
        await message.reply("#WANTFIX фото не найдено")
        return

    text = cuteCrop(page[1], 1000)

    await message.reply_photo(page[0], caption=text, parse_mode="HTML")
