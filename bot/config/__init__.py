from datetime import datetime

from .bot import bot, dp, router
from .config import (
    WIKI_COMMANDS,
    WIKIPEDIA_SHORTCUTS,
    is_test_session,
    settings,
)
from .languages import (
    GTRANSLATE_LANGS,
    LANGS,
    WIKIPEDIA_LANGS,
)
from .lib.locales import Locale
from .version import __version__

START_TIME = datetime.now()


__all__ = (
    settings,
    LANGS,
    GTRANSLATE_LANGS,
    WIKIPEDIA_LANGS,
    WIKI_COMMANDS,
    WIKIPEDIA_SHORTCUTS,
    bot,
    dp,
    router,
    Locale,
    is_test_session,
    __version__,
)
