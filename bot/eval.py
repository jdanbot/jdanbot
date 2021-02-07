from .config import bot, dp
from .lib.html import code

import traceback
import subprocess


async def print_(message, text):
    await message.reply(code("[print] " + str(text)), parse_mode="HTML")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["e"])
async def supereval(message):
    text = message.text.split(maxsplit=1)[1]

    async_ = "await" in text

    if async_:
        try:
            exec(
                "async def __ex(message, bot, print): " +
                "".join(f"\n {L}" for L in text.split("\n"))
            )
            await locals()["__ex"](message, bot, print_)
        except Exception:
            await message.reply(code(traceback.format_exc()),
                                parse_mode="HTML")
    else:
        try:

            exec(
                "def __ex(message, bot): " +
                "".join(f"\n {L}" for L in text.split("\n"))
            )
            locals()["__ex"](message, bot)

        except Exception:
            await message.reply(code(traceback.format_exc()),
                                parse_mode="HTML")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["jbash"])
async def bash(message):
    options = message.text.split(maxsplit=1)

    try:
        command = options[1].split()
        output = subprocess.check_output(command).decode("utf-8")

        await message.reply(code(output), parse_mode="HTML")
    except Exception:
        await message.reply(code(traceback.format_exc()),
                            parse_mode="HTML")
