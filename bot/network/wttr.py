from aiogram import types
from aiogram.utils.markdown import bold, code

from ..config import dp
from ..handlers.parse_arguments import parse_arguments_new
from ..lib.aioget import aioget
from ..lib.models import CustomField


@dp.message_handler(commands=["wttr", "weather"])
@parse_arguments_new
async def simple_test_func(
    message: types.Message,
    format: CustomField(int, default=3),
    query: CustomField(str)
):
    response = await aioget(f"https://wttr.in/{query}", params=dict(format=format))
    response_text = response.text.replace("   ", " ")

    if format in {3, 4}:
        text = (
            bold((parts := response_text.split(": "))[0].title())
            + ": "
            + code(parts[1])
        )
    else:
        text = code(response_text)

    await message.reply(text, parse_mode="markdownv2")
