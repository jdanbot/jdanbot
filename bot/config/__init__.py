from pytz import timezone

from .config import *         # noqa
from ..database import *      # noqa

from datetime import datetime

from .logger import logging   # noqa
from .vk_api import vk_api    # noqa
from .bot import bot, dp      # noqa
from .i18n import _           # noqa


START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")
SCHEDULE = any([BLOODYKNIGHT, RSS, VK, KATZ_BOTS, YOUTUBE])  # noqa
