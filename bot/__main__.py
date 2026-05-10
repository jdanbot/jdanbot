import asyncio
import builtins

from rich import print
from rich.traceback import install

from . import *  # noqa
from .config.bot import bot, dp, router
from .config.lib.i18n_middleware import i18nMiddleware
from .config.lib.spy_middleware import SpyMiddleware
from .database import setup_db

install(show_locals=True)
builtins.print = print


async def main() -> None:
    router.guest_message.middleware(
        middleware=SpyMiddleware()
    )
    router.message.middleware(middleware=SpyMiddleware())
    dp.update.outer_middleware(middleware=i18nMiddleware())

    dp.include_router(router)

    await setup_db()
    await dp.start_polling(bot, reset_webhook=True)


asyncio.run(main())
