import asyncio
import aioschedule

from aiogram import executor

from bot import *  # noqa
from bot.config import dp, DELAY, RSS
from bot.timer import rss_timer


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def scheduler():
    aioschedule.every(DELAY).seconds.do(rss_timer)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


async def startup(x):
    if RSS:
        asyncio.create_task(scheduler())


executor.start_polling(dp, loop=loop, on_startup=startup)
