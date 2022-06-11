from pytz import timezone
from datetime import datetime

from .config import settings, LOCALES_DIR, WIKICOMMANDS, UNIQUE_COMMANDS

from .languages import LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS

from .logger import logger   # noqa
from .bot import bot, dp
from .i18n import _


START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")


__all__ = (
    settings,
    LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS,
    LOCALES_DIR, WIKICOMMANDS,
    logger,
    bot, dp,
    _
)
