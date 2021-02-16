import asyncio
import re

from ..config import dp


async def calc(query):
    return eval(query, {"__builtins__": {}})


@dp.message_handler(commands=["calc"])
async def eban(message):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        await message.reply("Введите выражения для вычисления")
        return

    query = options[1]

    query = query.format(
        pi=3.14
    )

    match = re.search(r"[a-zA-Zа-яА-Я]", query)
    match_symbols = re.search(r"[\[\]\^\{\}]|\*\*", query)

    if type(match).__name__ == "Match":
        await message.reply("Только переменные и числа!")
        return

    if type(match_symbols).__name__ == "Match" and \
       message.from_user.id != 795449748:
        await message.reply("Только переменные и числа!")
        return

    try:
        result = await asyncio.wait_for(calc(query), 1)
    except Exception as e:
        print(e)
        result = "Timeout"

    await message.reply(str(result)[:4096])
