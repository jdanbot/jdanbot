from aiogram import types

import asyncio
from time import perf_counter

from ..config import dp
from ..lib.text import bold, code


@dp.message_handler(commands=["ping", "p"])
async def ping(message: types.Message):
    start = perf_counter()
    msg = await message.answer("⚾️ Think...")

    await msg.edit_text(bold("🏓 Pong ") + code("{time:.2f}s".format(
                            time=perf_counter() - start
                        )), parse_mode="HTML")

    await asyncio.sleep(3.5)

    await msg.delete()
    await message.delete()
