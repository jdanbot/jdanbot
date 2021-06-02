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

arch_class = "archwiki-template-meta-related-articles-start"

WIKIPYA_BLOCKLIST = [
    ["table", {"class": "infobox"}],
    ["ol", {"class": "references"}],

    ["link"], ["style"], ["img"],
    ["aside"], ["table"], ["br"],

    ["div", {"class": "tright"}],
    ["div", {"class": "plainlist"}],
    ["span", {"class": "mw-ext-cite-error"}],

    ["table", {"class": "sidebar"}],
    ["table", {"class": "lm-plashka"}],
    ["table", {"class": "lm-plashka-tiny"}],
    ["table", {"class": "tpl-quote-tiny"}],

    ["div", {"class": "thumbinner"}],
    ["div", {"class": "gallerytext"}],
    ["div", {"class": arch_class}],

    [None, {"class": "noprint"}],
    ["span", {"id": "w4g_rb_area-1"}]
]
