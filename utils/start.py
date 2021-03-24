import asyncio
import sys
from bot.config import dp

from aiogram import executor

from bot.vk import vk_timer

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def startup(x):
    await vk_timer()
    sys.exit()


executor.start_polling(dp, loop=loop, on_startup=startup)
