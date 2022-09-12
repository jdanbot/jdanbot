from ..config import dp
from ..lib.aioget import aioget

from aiogram.utils.markdown import bold, code

from aiogram import types


@dp.message_handler(commands=["wttr", "weather"])
async def download(message: types.Message):
    format, *query = message.get_args().split(" ", maxsplit=1)

    try:
        format = int(format)
        query = query[0]
    except:
        query = format
        format = 3

    response = await aioget(f"https://wttr.in/{query}", params=dict(format=format))
    response_text = response.text.replace("   ", " ")

    if format in {3, 4}:
        text = bold((parts := response_text.split(": "))[0].capitalize()) + ": " + code(parts[1])
    else:
        text = code(response_text)

    await message.reply(text, parse_mode="markdownv2")
