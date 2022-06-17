from dataclasses import dataclass
from typing import Any, Optional

from aiogram import types

from ..text import cute_crop


@dataclass
class Article:
    text: str
    image: Optional[str] = None
    keyboard: Optional[types.InlineKeyboardMarkup] = None
    parse_mode: str = "HTML"
    disable_web_page_preview: bool = False

    href: str = ""
    params: Any = None

    def __post_init__(self):
        TG_MESSAGE_LIMIT = 4096

        if (new_text := cute_crop(self.text, limit=TG_MESSAGE_LIMIT)) != "":
            self.text = new_text
        else:
            self.text[:TG_MESSAGE_LIMIT]
