import asyncio
from asyncio.events import AbstractEventLoop

from tortoise import run_async

from . import *  # noqa
from .config.bot import bot, dp, router
from .config.lib.middleware import (
    SpyMiddleware,
    TranslatorRunnerMiddleware,
)
from .database import setup_db


async def main() -> None:
    await setup_db()

    dp.update.outer_middleware(middleware=TranslatorRunnerMiddleware())
    router.message.middleware(middleware=SpyMiddleware())

    dp.include_router(router)

    await dp.start_polling(bot, reset_webhook=True)


loop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

run_async(main())
