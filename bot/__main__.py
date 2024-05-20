import asyncio

from . import *  # noqa
from .config import dp, bot, router
from .database.tables.connection import init_db
from .database import setup_db
from fluentogram import FluentTranslator, TranslatorHub
from fluent_compiler.bundle import FluentBundle

from pathlib import Path

from .config.lib.middleware import (
    TranslatorRunnerMiddleware,
    SpyMiddleware,
)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def main():
    translator_hub = TranslatorHub(
        {"ru": ("ru", "en"), "en": ("en",)},
        [
            FluentTranslator(
                "en",
                translator=FluentBundle.from_files(
                    "en_US", Path("./locales/en").glob("*.ftl")
                ),
            ),
            FluentTranslator(
                "ru",
                translator=FluentBundle.from_files(
                    "ru_RU", Path("./locales/ru").glob("*.ftl")
                ),
            ),
        ],
    )

    await init_db()
    await setup_db()
    dp.update.outer_middleware(TranslatorRunnerMiddleware())
    router.message.middleware(SpyMiddleware())

    dp.include_router(router)

    await dp.start_polling(
        bot, reset_webhook=True, _translator_hub=translator_hub
    )


asyncio.get_event_loop().run_until_complete(main())
