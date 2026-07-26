import asyncio

from . import *  # noqa
from .config.bot import COMMANDS, bot, dp, router
from .config.lib.i18n_middleware import i18nMiddleware
from .config.lib.spy_middleware import SpyMiddleware
from .database import MigratorService, setup_db

try:
    from rich import print
except ModuleNotFoundError:
    pass
else:
    import builtins

    builtins.print = print  # type: ignore[assignment]


async def main() -> None:
    router.guest_message.middleware(
        middleware=SpyMiddleware()
    )
    router.message.middleware(middleware=SpyMiddleware())
    dp.update.outer_middleware(middleware=i18nMiddleware())

    dp.include_router(router)

    MigratorService.activate_migrations()
    await setup_db()

    COMMANDS.parse_commands_from_router(router)
    await dp.start_polling(bot, reset_webhook=True)


asyncio.run(main())
