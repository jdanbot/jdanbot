from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import bold

from ..config import router
from ..filters import GetText
from ..lib.aioget import aioget


def to_celsius(grad: int) -> int:
    return int((grad - 32) / 1.8)


@router.message(Command("wttr", "weather"), GetText())
async def get_weather_func(
    message: types.Message, query: str
):
    response = await aioget(
        f"https://wttr.in/{query}?u", params=dict(format=1)
    )

    emoji, grads = (
        x.strip()
        for x in response.text.split(" ")
        if x != ""
    )

    if grads.endswith("F"):
        grads = f"{to_celsius(int(grads[0:-2]))}°C"

    if grads[0] not in {"-", "+"} and grads[0] != "0":
        grads = f"+{grads}"

    await message.reply(
        f"{emoji} {bold(query.title())} {grads}",
        parse_mode="markdown",
    )
