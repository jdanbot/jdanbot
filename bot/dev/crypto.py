import hashlib
from random import choice

from ..config import dp, _
from ..lib import handlers
from ..lib.text import code


@dp.message_handler(commands=["sha256"])
@handlers.get_text
async def sha256(message, text):
    text = bytearray(text.encode("utf-8"))
    crypt = hashlib.sha256(text).hexdigest()

    await message.reply(crypt)


@dp.message_handler(commands=["generate_password", "password"])
@handlers.parse_arguments(2)
async def password(message, options):
    try:
        password_len = int(options[1])
    except ValueError:
        await message.reply(_("error.pass_len_required"))
        return

    if password_len > 4096:
        await message.reply(_("errors.message_len"),
                            parse_mode="Markdown")
        return

    elif password_len < 6:
        await message.reply(_("errors.pass_crypt_is_low"),
                            parse_mode="Markdown")
        return

    password = ""
    symbols = []

    symbols.extend(list("abcdefghijklmnopqrstuvwxyz"))
    symbols.extend(list("abcdefghijklmnopqrstuvwxyz".upper()))
    symbols.extend(list('~!@#$%^&*()_+-=`[]\\}{|;\':"<>,./?'))
    symbols.extend(list("0123456789"))

    for __ in range(0, password_len):
        password += choice(symbols)

    await message.reply(code(password), parse_mode="HTML")
