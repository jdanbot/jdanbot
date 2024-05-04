import asyncio

from . import *  # noqa
from .config import dp
from .database.tables.connection import init_db

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def main():
    await init_db()
    await dp.start_polling(reset_webhook=True)


asyncio.get_event_loop().run_until_complete(main())
