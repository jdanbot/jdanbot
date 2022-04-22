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
    test: bool = False
    inline: bool = False

    params: Any = None

    def __post_init__(self):
        limit = 1024 if self.image and not self.test else 4096

        if (new_text := cute_crop(self.text, limit=limit)) != "":
            self.text = new_text
        else:
            self.text[:limit]
