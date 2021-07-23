import asyncio
import aioschedule

from aiogram import executor

from . import *  # noqa
from .config import (
    dp, Poll, DELAY, RSS, VK, SCHEDULE, 
    KATZ_BOTS, RSS_FEEDS, YOUTUBE, YOUTUBE_CHANNELS)
from .timer import rss_task, youtube_task
from .vk import vk_timer


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def scheduler():
    if RSS:
        for feed in RSS_FEEDS:
            aioschedule.every(DELAY).seconds.do(
                rss_task,
                feed["url"],
                feed["channelid"],
                feed["chatid"]
            )

    if VK:
        aioschedule.every(DELAY).seconds.do(vk_timer)

    if KATZ_BOTS:
        aioschedule.every(DELAY).seconds.do(Poll.close_old)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


async def startup(x):
    if SCHEDULE:
        asyncio.create_task(scheduler())


executor.start_polling(dp, loop=loop, on_startup=startup)
