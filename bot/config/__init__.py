import pendulum as pdl

from pytz import timezone

from .config import (
    settings,
    LOCALES_DIR,
    WIKI_COMMANDS,
    WIKIPEDIA_SHORTCUTS
)

from .languages import LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS

from .logger import logger
from .bot import bot, dp
from .i18n import _


START_TIME = pdl.now()
TIMEZONE = timezone("Europe/Moscow")


__all__ = (
    settings,
    LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS,
    LOCALES_DIR, WIKI_COMMANDS, WIKIPEDIA_SHORTCUTS,
    logger,
    bot, dp,
    _
)
