from .bot import dp
from .lib.html import code


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["calc"])
async def supereval(message):
    text = message.text.split(maxsplit=1)[1]
    await message.reply(code(str(eval(text))[:4000]),
                        parse_mode="HTML")
