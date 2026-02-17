import builtins
import asyncio
from asyncio.events import AbstractEventLoop

from rich.traceback import install
from rich import print
from tortoise import run_async

from . import *  # noqa
from .config.bot import bot, dp, router
from .config.lib.i18n_middleware import i18nMiddleware
from .config.lib.spy_middleware import SpyMiddleware
from .database import setup_db

install(show_locals=True)
builtins.print = print

async def main() -> None:
    await setup_db()

    dp.update.outer_middleware(middleware=i18nMiddleware())
    router.message.middleware(middleware=SpyMiddleware())

    dp.include_router(router)

    await dp.start_polling(bot, reset_webhook=True)


loop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

run_async(main())
