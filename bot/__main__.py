import asyncio
from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub
from tortoise import run_async

from . import *  # noqa
from .config import bot, dp, router
from .config.lib.middleware import (
    SpyMiddleware,
    TranslatorRunnerMiddleware,
)
from .database import setup_db

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

    await setup_db()

    dp.update.outer_middleware(TranslatorRunnerMiddleware())
    router.message.middleware(SpyMiddleware())

    dp.include_router(router)

    await dp.start_polling(
        bot, reset_webhook=True, _translator_hub=translator_hub
    )


run_async(main())
