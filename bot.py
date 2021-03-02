import asyncio
import aioschedule

from aiogram import executor

from bot import *  # noqa
from bot.config import dp, DELAY, ENABLE_RSS
from bot.timer import rss_task


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def scheduler():
    aioschedule.every(DELAY).seconds.do(rss_task)

    while True:
        await aioschedule.run_pending()


async def startup(x):
    if ENABLE_RSS:
        asyncio.create_task(scheduler())


executor.start_polling(dp, loop=loop, on_startup=startup)
