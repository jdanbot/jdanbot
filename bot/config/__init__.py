from whenever import Instant

from .bot import bot, dp, router
from .config import (
    WIKI_COMMANDS,
    WIKIPEDIA_SHORTCUTS,
    settings,
)
from .languages import (
    GTRANSLATE_LANGS,
    LANGS,
    WIKIPEDIA_LANGS,
)
from .lib.locales import Locale
from .logger import logger

START_TIME = Instant.now()


__all__ = (
    settings,
    LANGS,
    GTRANSLATE_LANGS,
    WIKIPEDIA_LANGS,
    WIKI_COMMANDS,
    WIKIPEDIA_SHORTCUTS,
    logger,
    bot,
    dp,
    router,
    Locale
)
