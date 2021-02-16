from art import text2art

from ..config import dp
from ..lib.html import code


@dp.message_handler(commands=["art"])
async def art(message):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        message.reply("Введи текст на английском для получения арта")
        return

    if len(options[1]) > 20:
        message.reply("Ты шизик.")
        return

    art = text2art(options[1], chr_ignore=True)

    await message.reply(code(art), parse_mode="HTML")
