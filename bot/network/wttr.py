from aiogram import types
from aiogram.utils.markdown import bold, code

from ..config import dp
from ..handlers.parse_arguments import parse_arguments_new
from ..lib.aioget import aioget
from ..lib.models import CustomField


def to_celsius(grad: int) -> int:
    return int((grad - 32) / 1.8)


@dp.message_handler(commands=["wttr", "weather"])
@parse_arguments_new
async def simple_test_func(
    message: types.Message,
    format: CustomField(int, default=3),
    query: CustomField(str)
):
    response = await aioget(
        f"https://wttr.in/{query}?u", params=dict(format=1)
    )

    emoji, grads = [
        x.strip()
        for x in response.text.split(" ")
        if x != ""
    ]

    if grads.endswith("F"):
        grads = f"{to_celsius(int(grads[0:-2]))}°C"

    if grads[0] not in {"-", "+"} and grads[0] != "0":
        grads = f"+{grads}"

    await message.reply(
        f"{emoji} {bold(query.title())} {grads}",
        parse_mode="markdown",
    )