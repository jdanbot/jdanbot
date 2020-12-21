from .bot import bot, dp
from .lib.html import code

import traceback


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
                "async def __ex(message, print): " +
                "".join(f"\n {L}" for L in text.split("\n"))
            )
            await locals()["__ex"](message, print_)
        except:
            await message.reply(code(traceback.format_exc()),
                                parse_mode="HTML")
    else:
        try:

            exec(
                "def __ex(message): " +
                "".join(f"\n {L}" for L in text.split("\n"))
            )
            locals()["__ex"](message)

        except:
            await message.reply(code(traceback.format_exc()),
                                parse_mode="HTML")
