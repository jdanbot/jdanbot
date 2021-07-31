import asyncio
from time import perf_counter

from ..config import dp
from ..lib.text import bold, code

@dp.message_handler(commands=["ping", "p"])
async def ping(message):
    start = perf_counter()
    msg = await message.answer("⚾️ Think...")
    end = perf_counter()
    await msg.edit_text(bold("🏓 Pong ") + code(round(end - start, 3)) + code("s"),
                        parse_mode="HTML")
