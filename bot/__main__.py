import asyncio

from aiogram import executor

from . import *  # noqa
from .config import dp
from .schemas import db_setup
from .lib.schedule import schedule_setup

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def startup(x):
    db_setup()
    schedule_setup()


executor.start_polling(dp, loop=loop, on_startup=startup)
