from pytz import timezone

import logging

from .config import *
from .database import *

from datetime import datetime

from .logger import logging
from .vk_api import vk_api
from .bot import bot, dp
from .i18n import _

START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")
SCHEDULE = RSS or VK or KATZ_BOTS or YOUTUBE

WIKIPYA_BLOCKLIST = [
    ["table", {"class": "infobox"}],
    ["ol", {"class": "references"}],
    ["link"], ["style"], ["img"],
    ["div", {"class": "tright"}],
    ["table", {"class": "noprint"}],
    ["div", {"class": "plainlist"}],
    ["table", {"class": "sidebar"}],
    ["span", {"class": "mw-ext-cite-error"}]
]
