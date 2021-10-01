from pytz import timezone

from .config import *  # noqa
from ..database import *  # noqa

from datetime import datetime

START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")
SCHEDULE = any([BLOODYKNIGHT, RSS, VK, KATZ_BOTS, YOUTUBE])

arch_class = "archwiki-template-meta-related-articles-start"

WIKIPYA_BLOCKLIST = [
    ["ol", {"class": "references"}],
    [None, {"class": "reference"}],

    ["link"], ["style"], ["img"],
    ["aside"], ["table"], ["br"],
    ["span", {"class": "mw-ext-cite-error"}],

    ["div", {"class": "thumbinner"}],
    ["div", {"class": "gallerytext"}],
    ["div", {"class": arch_class}],
    ["div", {"class": "tright"}],
    ["div", {"class": "plainlist"}],
    ["div", {"class": "gametabs"}],

    [None, {"class": "noprint"}],
    ["span", {"id": "w4g_rb_area-1"}],

    ["p", {"class": "caption"}],
]
