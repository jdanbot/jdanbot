from pytz import timezone
from datetime import datetime

from .config import settings, LOCALES_DIR, WIKI_COMMANDS, WIKIPEDIA_SHORTCUTS

from .languages import LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS

from .logger import logger   # noqa
from .bot import bot, dp
from .i18n import _


START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")


__all__ = (
    settings,
    LANGS, GTRANSLATE_LANGS, WIKIPEDIA_LANGS,
    LOCALES_DIR, WIKI_COMMANDS, WIKIPEDIA_SHORTCUTS,
    logger,
    bot, dp,
    _
)
