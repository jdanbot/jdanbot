import asyncio

from aiogram import executor

from bot import *  # noqa
from bot.config import dp, DELAY, ENABLE_RSS
from bot.timer import timer, repeat

loop = asyncio.get_event_loop()

if ENABLE_RSS:
    loop.call_later(DELAY, repeat, timer, loop)

executor.start_polling(dp, loop=loop)
