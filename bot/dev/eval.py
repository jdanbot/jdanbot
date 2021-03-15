import traceback
import subprocess

from ..config import bot, dp
from ..lib.text import code


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["e"])
async def supereval(message):
    code = message.text.split(maxsplit=1)[1]

    exec(
        "async def __ex(message, bot): " +
        "".join(f"\n {L}" for L in code.split("\n"))
    )

    try:
        await locals()["__ex"](message, bot)
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
