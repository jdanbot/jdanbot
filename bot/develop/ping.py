import asyncio
from time import perf_counter

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import bold, code

from ..config import router


@router.message(Command("ping", "p"))
async def ping(message: types.Message):
    start = perf_counter()
    msg = await message.answer("⚾️ Think...", parse_mode=None)

    time = perf_counter() - start

    await msg.edit_text(
        f"{bold("🏓 Pong")} {code(f"{time:.2f}s")}",
    )

    await asyncio.sleep(3.5)

    await msg.delete()
    await message.delete()
