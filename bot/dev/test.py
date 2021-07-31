import asyncio
from time import perf_counter

from ..config import dp
from ..lib.text import bold, code

@dp.message_handler(commands=["ping", "p"])
async def ping(message):
    start = perf_counter()
    msg = await bot.send_message(message.chat.id, "Think...")
    end = perf_counter()
    ping = end - start
    await msg.edit_text(f'<bold>Pong</bold><code> {round(ping, 3)}s</code>'.format(pings={round(ping, 3)}), parse_mode="HTML")
