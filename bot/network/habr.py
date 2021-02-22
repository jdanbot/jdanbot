from ..config import dp
from ..lib import handlers
from ..lib.habr import Habr


@dp.message_handler(commands=["habr"])
@handlers.parse_arguments(1)
async def habr(message, params):
    try:
        id_ = int(params[1])

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
