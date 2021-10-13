import asyncio
from bot.network.mono import monobank
import aioschedule

from aiogram import executor, types

from . import *  # noqa
from .config import (
    dp, Poll, DELAY, RSS, VK, SCHEDULE,
    KATZ_BOTS, RSS_FEEDS, BLOODYKNIGHT)
from .timer import rss_task
from .vk import vk_timer


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def scheduler():
    if RSS:
        for feed in RSS_FEEDS:
            aioschedule.every(DELAY).seconds.do(
                rss_task,
                feed["url"],
                feed["feed_id"],
                feed["chat_id"]
            )

    if VK:
        aioschedule.every(DELAY).seconds.do(vk_timer)

    if KATZ_BOTS:
        aioschedule.every(DELAY).seconds.do(Poll.close_old)

    if BLOODYKNIGHT:
        message = types.Message(chat=types.Chat(id=-1001410092459))
        aioschedule.every().day.at("8:00").do(monobank, message)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


async def startup(x):
    if SCHEDULE:
        asyncio.create_task(scheduler())


executor.start_polling(dp, loop=loop, on_startup=startup)
