from aiogram import types

from ..config import dp
from ..lib.aioget import aioget


@dp.message_handler(commands=["navalny"])
async def navalny(message: types.Message):
    res = await aioget("https://free.navalny.com/api/v1/maps/counters/")
    await message.reply(res.json()["persons"])
