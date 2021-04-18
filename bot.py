import asyncio
import aioschedule

from aiogram import executor

from bot import *  # noqa
from bot.config import dp, polls, DELAY, RSS, VK, SCHEDULE, KATZ_BOTS
from bot.timer import rss_timer
from bot.vk import vk_timer


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def scheduler():
    if RSS:
        aioschedule.every(DELAY).seconds.do(rss_timer)
    if VK:
        aioschedule.every(DELAY).seconds.do(vk_timer)
    if KATZ_BOTS:
        aioschedule.every(DELAY).seconds.do(polls.close_old)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


async def startup(x):
    if SCHEDULE:
        asyncio.create_task(scheduler())


executor.start_polling(dp, loop=loop, on_startup=startup)
