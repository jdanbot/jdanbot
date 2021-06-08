import traceback
import subprocess

from ..config import bot, dp
from ..lib.text import code
from ..lib import handlers


@handlers.only_jdan
@dp.message_handler(commands=["e"])
async def supereval(message):
    command, query = message.text.split(maxsplit=1)

    q = [f"\n {line}" for line in query.split("\n")]
    q[-1] = q[-1].replace("\n ", "\n return ")

    exec(
        "async def __ex(message, bot): " +
        "".join(q)
    )

    try:
        output = await locals()["__ex"](message, bot)
    except Exception:
        output = traceback.format_exc()

    if output == "disable_stdout":
        return

    await message.reply(code(output),
                        parse_mode="HTML")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["jbash"])
async def bash(message):
    options = message.text.split(maxsplit=1)

    try:
        command = options[1].split()
        output = subprocess.check_output(command).decode("utf-8")

    except Exception:
        output = traceback.format_exc()

    await message.reply(code(str(output)),
                        parse_mode="HTML")
