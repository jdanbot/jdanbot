from ..config import bot, dp
from ..lib.html import code
from ..data import data

from random import choice

import hashlib


@dp.message_handler(commands=["sha256"])
async def sha256(message):
    text = ""

    if message.reply_to_message:
        reply = message.reply_to_message

        if reply.text:
            text = reply.text.encode("utf-8")

        elif reply.document:
            file_id = reply.document.file_id

            document = bot.get_file(file_id)
            text = bot.download_file(document.file_path)
    else:
        opt = message.text.split(maxsplit=1)

        if len(opt) == 1:
            await message.reply("Ответьте на сообщение с текстом")
            return

        text = opt[1].encode("utf-8")

    await message.reply(hashlib.sha256(bytearray(text)).hexdigest())


@dp.message_handler(commands=["generate_password"])
async def password(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 1:
        await message.reply_to("Укажите количество символов в пароле")
        return

    try:
        crypto_type = int(opt[1])
    except ValueError:
        message.reply("Введите число")
        return

    if crypto_type > 4096:
        await message.reply(data["errors"]["message_len"],
                            parse_mode="Markdown")
        return

    elif crypto_type < 6:
        message.reply("Пароли меньше `6` символов запрещены",
                      parse_mode="Markdown")
        return

    password = ""
    symbols = []

    symbols.extend(list("abcdefghijklmnopqrstuvwxyz"))
    symbols.extend(list("abcdefghijklmnopqrstuvwxyz".upper()))
    symbols.extend(list('~!@#$%^&*()_+-=`[]\\}{|;\':"<>,./?'))
    symbols.extend(list("0123456789"))

    for num in range(0, crypto_type):
        password += choice(symbols)

    await message.reply(code(password), parse_mode="HTML")
