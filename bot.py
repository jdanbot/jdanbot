import asyncio

from aiogram import executor

from bot import *  # noqa
from bot.config import dp, DELAY, ENABLE_RSS
from bot.timer import timer, repeat

try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

if ENABLE_RSS:
    loop.call_later(DELAY, repeat, timer, loop)

executor.start_polling(dp, loop=loop)
