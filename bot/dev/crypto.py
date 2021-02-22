import hashlib
from random import choice

from ..config import dp
from ..data import data
from ..lib import handlers
from ..lib.html import code


@dp.message_handler(commands=["sha256"])
@handlers.get_text
async def sha256(message, text):
    text = bytearray(text.encode("utf-8"))
    crypt = hashlib.sha256(text).hexdigest()

    await message.reply(crypt)


@dp.message_handler(commands=["generate_password"])
@handlers.parse_arguments(1)
async def password(message, options):
    try:
        password_len = int(options[1])
    except ValueError:
        await message.reply("Введите число")
        return

    if password_len > 4096:
        await message.reply(data.errors.message_len,
                            parse_mode="Markdown")
        return

    elif password_len < 6:
        await message.reply("Пароли меньше `6` символов запрещены",
                            parse_mode="Markdown")
        return

    password = ""
    symbols = []

    symbols.extend(list("abcdefghijklmnopqrstuvwxyz"))
    symbols.extend(list("abcdefghijklmnopqrstuvwxyz".upper()))
    symbols.extend(list('~!@#$%^&*()_+-=`[]\\}{|;\':"<>,./?'))
    symbols.extend(list("0123456789"))

    for _ in range(0, password_len):
        password += choice(symbols)

    await message.reply(code(password), parse_mode="HTML")
