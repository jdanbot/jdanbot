from pytz import timezone

import logging
from datetime import datetime

from .config import DELAY, VK, RSS, IMAGE_PATH, RSS_FEEDS, VK_CHANNELS, STATUS, KATZ_BOTS, YOUTUBE, YOUTUBE_CHANNELS, YOUTUBE_KEY
from .database import events, videos, warns, notes, pidors, pidorstats, polls, conn
from .logger import logging
from .vk_api import vk_api
from .bot import bot, dp

START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")
SCHEDULE = RSS or VK or KATZ_BOTS or YOUTUBE
