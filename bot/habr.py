from .bot import dp
from .lib.habr import Habr


@dp.message_handler(commands=["habr"])
async def habr(message):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        await message.reply("Введи id поста из хабра")
        return

    try:
        id_ = int(options[-1])

    except ValueError:
        await message.reply("Введи валидный id поста")

    h = Habr()

    try:
        habrPage = await h.page(id_)
        await message.reply(habrPage[:4096],
                            parse_mode="HTML",
                            disable_web_page_preview=True)

    except Exception as e:
        await message.reply(e)
