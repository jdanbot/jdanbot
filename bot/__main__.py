import asyncio

from aiogram import executor

from . import *  # noqa
from .config import dp
from .schemas import db_setup
from .lib.schedule import schedule_setup

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def startup():
    db_setup()
    schedule_setup()


async def main():
    await startup()
    await dp.start_polling(reset_webhook=True)

asyncio.get_event_loop().run_until_complete(main())
