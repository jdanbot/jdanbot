import re

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import bold, code

from ..config import router
from ..filters import GetText
from ..lib.aioget import aioget


@router.message(Command("wttr", "weather"), GetText())
async def get_weather_func(message: types.Message, query: str):
    response = await aioget(
        f"https://wttr.in/{query}", params=dict(format=3)
    )
    city, weather = map(
        lambda x: x.strip(),
        re.sub(" +", " ", response.text).split(": "),
    )

    await message.reply(f"{bold(city.title())}: {code(weather)}")
